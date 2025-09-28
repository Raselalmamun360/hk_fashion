from django.test import TestCase
from django.urls import reverse
from .models import Category, Product
from decimal import Decimal

class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )
    
    def test_category_creation(self):
        self.assertEqual(self.category.name, 'Test Category')
        self.assertEqual(self.category.slug, 'test-category')
    
    def test_category_str_representation(self):
        self.assertEqual(str(self.category), 'Test Category')
    
    def test_get_absolute_url(self):
        url = self.category.get_absolute_url()
        self.assertEqual(url, '/products/test-category/')

class ProductModelTest(TestCase):
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
            available=True,
            is_preorder=False
        )
        
        self.preorder_product = Product.objects.create(
            category=self.category,
            name='Preorder Product',
            slug='preorder-product',
            description='Preorder description',
            price=Decimal('149.99'),
            stock=0,
            available=True,
            is_preorder=True
        )
    
    def test_product_creation(self):
        self.assertEqual(self.product.name, 'Test Product')
        self.assertEqual(self.product.price, Decimal('99.99'))
        self.assertEqual(self.product.stock, 10)
        self.assertTrue(self.product.available)
        self.assertFalse(self.product.is_preorder)
    
    def test_preorder_product_creation(self):
        self.assertEqual(self.preorder_product.name, 'Preorder Product')
        self.assertEqual(self.preorder_product.price, Decimal('149.99'))
        self.assertEqual(self.preorder_product.stock, 0)
        self.assertTrue(self.preorder_product.available)
        self.assertTrue(self.preorder_product.is_preorder)
    
    def test_product_str_representation(self):
        self.assertEqual(str(self.product), 'Test Product')
    
    def test_get_absolute_url(self):
        url = self.product.get_absolute_url()
        self.assertEqual(url, f'/products/{self.product.id}/test-product/')

class ProductViewsTest(TestCase):
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
    
    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertContains(response, 'Test Product')
    
    def test_product_list_view(self):
        response = self.client.get(reverse('products:product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product_list.html')
        self.assertContains(response, 'Test Product')
    
    def test_product_list_by_category_view(self):
        response = self.client.get(reverse('products:product_list_by_category', args=['test-category']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product_list.html')
        self.assertContains(response, 'Test Product')
    
    def test_product_detail_view(self):
        response = self.client.get(reverse('products:product_detail', args=[self.product.id, 'test-product']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product_detail.html')
        self.assertContains(response, 'Test Product')
        self.assertContains(response, '99.99')