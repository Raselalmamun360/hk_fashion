import random
from django.core.management.base import BaseCommand
from django.core.files import File
from django.utils.text import slugify
from products.models import Category, Product
from datetime import datetime, timedelta
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Create demo products with realistic data'

    def handle(self, *args, **options):
        # Create categories if they don't exist
        categories_data = [
            "Men's T-Shirts", "Men's Shirts", "Men's Jeans", "Men's Jackets",
            "Women's Dresses", "Women's Tops", "Women's Jeans", "Women's Jackets",
            "Accessories", "Shoes"
        ]
        
        categories = []
        for cat_name in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_name,
                defaults={'slug': slugify(cat_name)}
            )
            categories.append(category)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category: {cat_name}'))
        
        # Demo products data
        products_data = [
            # Men's T-Shirts
            {
                'name': 'Classic White T-Shirt',
                'category': "Men's T-Shirts",
                'price': 24.99,
                'stock': 50,
                'description': 'A classic white t-shirt made from 100% cotton. Perfect for casual wear.',
                'colors': ['White'],
                'sizes': ['S', 'M', 'L', 'XL']
            },
            {
                'name': 'Graphic Print T-Shirt',
                'category': "Men's T-Shirts",
                'price': 29.99,
                'stock': 35,
                'description': 'Trendy graphic print t-shirt with a comfortable fit.',
                'colors': ['Black', 'Navy'],
                'sizes': ['M', 'L', 'XL']
            },
            # Men's Shirts
            {
                'name': 'Slim Fit Dress Shirt',
                'category': "Men's Shirts",
                'price': 49.99,
                'stock': 25,
                'description': 'Elegant slim fit dress shirt for formal occasions.',
                'colors': ['White', 'Light Blue'],
                'sizes': ['S', 'M', 'L']
            },
            # Women's Dresses
            {
                'name': 'Floral Summer Dress',
                'category': "Women's Dresses",
                'price': 59.99,
                'stock': 30,
                'description': 'Beautiful floral summer dress perfect for warm days.',
                'colors': ['Floral', 'Blue'],
                'sizes': ['XS', 'S', 'M']
            },
            # Women's Tops
            {
                'name': 'Basic Crop Top',
                'category': "Women's Tops",
                'price': 19.99,
                'stock': 45,
                'description': 'Comfortable and stylish crop top for casual wear.',
                'colors': ['Black', 'White', 'Pink'],
                'sizes': ['XS', 'S', 'M']
            },
            # Jeans
            {
                'name': 'Slim Fit Jeans',
                'category': "Men's Jeans",
                'price': 69.99,
                'stock': 20,
                'description': 'Classic slim fit jeans made from premium denim.',
                'colors': ['Blue', 'Black'],
                'sizes': ['28', '30', '32', '34']
            },
            {
                'name': 'Skinny Jeans',
                'category': "Women's Jeans",
                'price': 64.99,
                'stock': 28,
                'description': 'Stylish skinny jeans with a comfortable stretch.',
                'colors': ['Blue', 'Black', 'Light Blue'],
                'sizes': ['24', '26', '28', '30']
            },
            # Jackets
            {
                'name': 'Bomber Jacket',
                'category': "Men's Jackets",
                'price': 89.99,
                'stock': 15,
                'description': 'Classic bomber jacket with a modern fit.',
                'colors': ['Black', 'Olive'],
                'sizes': ['S', 'M', 'L', 'XL']
            },
            # Accessories
            {
                'name': 'Leather Belt',
                'category': 'Accessories',
                'price': 34.99,
                'stock': 40,
                'description': 'Genuine leather belt with a sleek buckle.',
                'colors': ['Black', 'Brown'],
                'sizes': ['S/M', 'L/XL']
            },
            # Shoes
            {
                'name': 'Casual Sneakers',
                'category': 'Shoes',
                'price': 79.99,
                'stock': 22,
                'is_preorder': True,
                'preorder_release_date': (datetime.now() + timedelta(days=14)).date(),
                'description': 'Comfortable and stylish casual sneakers for everyday wear.',
                'colors': ['White', 'Black'],
                'sizes': ['7', '8', '9', '10', '11', '12']
            }
        ]

        # Create products
        for product_data in products_data:
            category_name = product_data.pop('category')
            colors = product_data.pop('colors', [])
            sizes = product_data.pop('sizes', [])
            is_preorder = product_data.pop('is_preorder', False)
            preorder_date = product_data.pop('preorder_release_date', None)
            
            # Create a slug from the product name
            slug = slugify(product_data['name'])
            
            # Get or create the product
            product, created = Product.objects.get_or_create(
                name=product_data['name'],
                defaults={
                    'category': Category.objects.get(name=category_name),
                    'slug': slug,
                    'price': product_data['price'],
                    'stock': product_data['stock'],
                    'description': product_data['description'],
                    'is_preorder': is_preorder,
                    'preorder_release_date': preorder_date if is_preorder else None
                }
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created product: {product.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Product already exists: {product.name}'))
        
        self.stdout.write(self.style.SUCCESS('Successfully created demo products!'))
