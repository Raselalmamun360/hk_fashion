import os
import django
import random
from decimal import Decimal

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hk_fashion.settings')
django.setup()

from django.contrib.auth.models import User
from products.models import Category, Product
from django.utils.text import slugify
from django.core.management import call_command

def create_superuser():
    """Create a superuser if it doesn't exist"""
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print('Superuser created successfully')
    else:
        print('Superuser already exists')

def create_categories():
    """Create sample categories"""
    categories = [
        'Men\'s Clothing',
        'Women\'s Clothing',
        'Accessories',
        'Footwear',
        'Jewelry'
    ]
    
    created_categories = []
    
    for category_name in categories:
        slug = slugify(category_name)
        category, created = Category.objects.get_or_create(
            name=category_name,
            slug=slug
        )
        created_categories.append(category)
        if created:
            print(f'Category created: {category_name}')
        else:
            print(f'Category already exists: {category_name}')
    
    return created_categories

def create_products(categories):
    """Create sample products for each category"""
    products_data = [
        # Men's Clothing
        {
            'category': 'Men\'s Clothing',
            'products': [
                {
                    'name': 'Classic White Shirt',
                    'price': '29.99',
                    'description': 'A timeless white shirt for any occasion.',
                    'stock': 50,
                    'is_preorder': False
                },
                {
                    'name': 'Slim Fit Jeans',
                    'price': '49.99',
                    'description': 'Comfortable slim fit jeans for everyday wear.',
                    'stock': 30,
                    'is_preorder': False
                },
                {
                    'name': 'Designer Blazer',
                    'price': '129.99',
                    'description': 'Elegant blazer for formal occasions.',
                    'stock': 15,
                    'is_preorder': False
                },
                {
                    'name': 'Limited Edition Jacket',
                    'price': '199.99',
                    'description': 'Exclusive limited edition jacket. Pre-order now!',
                    'stock': 0,
                    'is_preorder': True
                }
            ]
        },
        # Women's Clothing
        {
            'category': 'Women\'s Clothing',
            'products': [
                {
                    'name': 'Summer Dress',
                    'price': '39.99',
                    'description': 'Light and comfortable dress for summer days.',
                    'stock': 40,
                    'is_preorder': False
                },
                {
                    'name': 'Elegant Blouse',
                    'price': '34.99',
                    'description': 'Stylish blouse for work or casual outings.',
                    'stock': 25,
                    'is_preorder': False
                },
                {
                    'name': 'Designer Skirt',
                    'price': '59.99',
                    'description': 'Fashionable skirt for any occasion.',
                    'stock': 20,
                    'is_preorder': False
                },
                {
                    'name': 'Exclusive Evening Gown',
                    'price': '249.99',
                    'description': 'Stunning evening gown from our upcoming collection. Pre-order now!',
                    'stock': 0,
                    'is_preorder': True
                }
            ]
        },
        # Accessories
        {
            'category': 'Accessories',
            'products': [
                {
                    'name': 'Leather Belt',
                    'price': '24.99',
                    'description': 'High-quality leather belt.',
                    'stock': 60,
                    'is_preorder': False
                },
                {
                    'name': 'Silk Scarf',
                    'price': '19.99',
                    'description': 'Elegant silk scarf with unique patterns.',
                    'stock': 45,
                    'is_preorder': False
                },
                {
                    'name': 'Designer Sunglasses',
                    'price': '89.99',
                    'description': 'Stylish sunglasses for the summer.',
                    'stock': 30,
                    'is_preorder': False
                }
            ]
        },
        # Footwear
        {
            'category': 'Footwear',
            'products': [
                {
                    'name': 'Casual Sneakers',
                    'price': '59.99',
                    'description': 'Comfortable sneakers for everyday use.',
                    'stock': 35,
                    'is_preorder': False
                },
                {
                    'name': 'Formal Shoes',
                    'price': '79.99',
                    'description': 'Elegant formal shoes for special occasions.',
                    'stock': 25,
                    'is_preorder': False
                },
                {
                    'name': 'Limited Edition Boots',
                    'price': '149.99',
                    'description': 'Exclusive boots from our upcoming collection. Pre-order now!',
                    'stock': 0,
                    'is_preorder': True
                }
            ]
        },
        # Jewelry
        {
            'category': 'Jewelry',
            'products': [
                {
                    'name': 'Silver Necklace',
                    'price': '49.99',
                    'description': 'Elegant silver necklace for any occasion.',
                    'stock': 20,
                    'is_preorder': False
                },
                {
                    'name': 'Gold Earrings',
                    'price': '69.99',
                    'description': 'Beautiful gold earrings to complement your style.',
                    'stock': 15,
                    'is_preorder': False
                },
                {
                    'name': 'Diamond Ring',
                    'price': '299.99',
                    'description': 'Stunning diamond ring for special moments.',
                    'stock': 10,
                    'is_preorder': False
                },
                {
                    'name': 'Limited Collection Bracelet',
                    'price': '199.99',
                    'description': 'Exclusive bracelet from our upcoming collection. Pre-order now!',
                    'stock': 0,
                    'is_preorder': True
                }
            ]
        }
    ]
    
    for product_category in products_data:
        category_name = product_category['category']
        category = next((c for c in categories if c.name == category_name), None)
        
        if not category:
            continue
        
        for product_data in product_category['products']:
            name = product_data['name']
            slug = slugify(name)
            
            product, created = Product.objects.get_or_create(
                name=name,
                defaults={
                    'category': category,
                    'slug': slug,
                    'price': Decimal(product_data['price']),
                    'description': product_data['description'],
                    'stock': product_data['stock'],
                    'is_preorder': product_data['is_preorder'],
                    'available': True
                }
            )
            
            if created:
                print(f'Product created: {name}')
            else:
                print(f'Product already exists: {name}')

def main():
    """Main function to populate the database"""
    print('Starting database population...')
    
    # Create superuser
    create_superuser()
    
    # Create categories
    categories = create_categories()
    
    # Create products
    create_products(categories)
    
    print('Database population completed!')

if __name__ == '__main__':
    main()