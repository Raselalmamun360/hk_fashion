from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from products.models import Category, Product
from .models import Order, OrderItem
from decimal import Decimal

class OrderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
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
        
        self.order = Order.objects.create(
            user=self.user,
            first_name='Test',
            last_name='User',
            email='test@example.com',
            address='123 Test St',
            postal_code='12345',
            city='Test City'
        )
        
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            price=Decimal('99.99'),
            quantity=2
        )
    
    def test_order_creation(self):
        self.assertEqual(self.order.first_name, 'Test')
        self.assertEqual(self.order.last_name, 'User')
        self.assertEqual(self.order.email, 'test@example.com')
        self.assertEqual(self.order.status, 'pending')
    
    def test_order_str_representation(self):
        self.assertEqual(str(self.order), f'Order {self.order.id}')
    
    def test_order_get_total_cost(self):
        expected_cost = Decimal('99.99') * 2
        self.assertEqual(self.order.get_total_cost(), expected_cost)
    
    def test_order_item_creation(self):
        self.assertEqual(self.order_item.product, self.product)
        self.assertEqual(self.order_item.price, Decimal('99.99'))
        self.assertEqual(self.order_item.quantity, 2)
    
    def test_order_item_get_cost(self):
        expected_cost = Decimal('99.99') * 2
        self.assertEqual(self.order_item.get_cost(), expected_cost)

class OrderViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
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
        
        self.order = Order.objects.create(
            user=self.user,
            first_name='Test',
            last_name='User',
            email='test@example.com',
            address='123 Test St',
            postal_code='12345',
            city='Test City'
        )
        
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            price=Decimal('99.99'),
            quantity=2
        )
    
    def test_order_create_view_get(self):
        # First add a product to the cart
        self.client.post(
            reverse('cart:cart_add', args=[self.product.id]),
            {'quantity': 1, 'override': False}
        )
        
        response = self.client.get(reverse('orders:order_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/order_create.html')
    
    def test_order_create_view_post(self):
        # First add a product to the cart
        self.client.post(
            reverse('cart:cart_add', args=[self.product.id]),
            {'quantity': 1, 'override': False}
        )
        
        # Then create an order
        order_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'address': '123 Main St',
            'postal_code': '54321',
            'city': 'New City'
        }
        
        response = self.client.post(reverse('orders:order_create'), order_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/order_created.html')
        
        # Check if order was created
        new_order = Order.objects.filter(email='john@example.com').first()
        self.assertIsNotNone(new_order)
        self.assertEqual(new_order.first_name, 'John')
        self.assertEqual(new_order.last_name, 'Doe')
    
    def test_order_history_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('orders:order_history'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/order_history.html')
        
        # Check if the order ID is in the response content as text
        self.assertContains(response, str(self.order.id))
    
    def test_order_detail_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('orders:order_detail', args=[self.order.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/order_detail.html')
        self.assertContains(response, 'Test Product')
        self.assertContains(response, '99.99')