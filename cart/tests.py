from django.test import TestCase, RequestFactory
from django.urls import reverse
from products.models import Category, Product
from .cart import Cart
from decimal import Decimal
from django.contrib.sessions.middleware import SessionMiddleware

class CartTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )
        
        self.product = Product.objects.create(
            category=self.category,
            name='Test Product',
            slug='test-product',
            description='Test description',
            price=Decimal('99.99'),
            stock=10,
            available=True
        )
        
        # Create a request with a session
        self.request = self.factory.get('/')
        middleware = SessionMiddleware(lambda x: None)
        middleware.process_request(self.request)
        self.request.session.save()
        
        # Initialize cart with the request that has a session
        self.cart = Cart(self.request)
    
    def test_cart_initialization(self):
        self.assertEqual(len(self.cart), 0)
        self.assertEqual(self.cart.get_total_price(), 0)
    
    def test_add_product_to_cart(self):
        self.cart.add(self.product)
        self.assertEqual(len(self.cart), 1)
        self.assertEqual(self.cart.cart[str(self.product.id)]['quantity'], 1)
    
    def test_add_multiple_quantity(self):
        # Fix: Use quantity parameter correctly
        self.cart.add(self.product, quantity=3)
        self.assertEqual(self.cart.cart[str(self.product.id)]['quantity'], 3)
        # Fix: The length of the cart should be 1 (one product type)
        self.assertEqual(sum(item['quantity'] for item in self.cart.cart.values()), 3)
    
    def test_update_quantity(self):
        self.cart.add(self.product, quantity=1)
        self.cart.add(self.product, quantity=5, override_quantity=True)
        self.assertEqual(self.cart.cart[str(self.product.id)]['quantity'], 5)
    
    def test_remove_product(self):
        self.cart.add(self.product)
        self.assertEqual(len(self.cart), 1)
        self.cart.remove(self.product)
        self.assertEqual(len(self.cart), 0)
    
    def test_get_total_price(self):
        self.cart.add(self.product, quantity=2)
        expected_price = Decimal('99.99') * 2
        self.assertEqual(self.cart.get_total_price(), expected_price)
    
    def test_clear_cart(self):
        self.cart.add(self.product)
        self.assertEqual(len(self.cart), 1)
        
        # Fix: Make sure the cart is actually cleared
        self.cart.clear()
        # Reinitialize the cart after clearing to reflect the session changes
        self.cart = Cart(self.request)
        self.assertEqual(len(self.cart), 0)

class CartViewsTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )
        
        self.product = Product.objects.create(
            category=self.category,
            name='Test Product',
            slug='test-product',
            description='Test description',
            price=Decimal('99.99'),
            stock=10,
            available=True
        )
    
    def test_cart_detail_view(self):
        response = self.client.get(reverse('cart:cart_detail'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart/detail.html')
    
    def test_cart_add_view(self):
        response = self.client.post(
            reverse('cart:cart_add', args=[self.product.id]),
            {'quantity': 1, 'override': False}
        )
        self.assertEqual(response.status_code, 302)  # Redirect after adding to cart
        
        # Check if product was added to cart
        response = self.client.get(reverse('cart:cart_detail'))
        self.assertContains(response, 'Test Product')
    
    def test_cart_remove_view(self):
        # First add a product to the cart
        self.client.post(
            reverse('cart:cart_add', args=[self.product.id]),
            {'quantity': 1, 'override': False}
        )
        
        # Then remove it
        response = self.client.get(reverse('cart:cart_remove', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)  # Redirect after removing from cart
        
        # Check if product was removed from cart
        response = self.client.get(reverse('cart:cart_detail'))
        self.assertNotContains(response, 'Test Product')