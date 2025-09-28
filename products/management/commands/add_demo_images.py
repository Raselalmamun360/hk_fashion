import os
import requests
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from products.models import Product
from django.conf import settings

class Command(BaseCommand):
    help = 'Adds demo images to products from a placeholder service'

    def handle(self, *args, **options):
        # List of placeholder image URLs (using placeholder.com with fashion-related keywords)
        image_urls = [
            'https://picsum.photos/800/1000?random=1',  # Fashion 1
            'https://picsum.photos/800/1000?random=2',  # Fashion 2
            'https://picsum.photos/800/1000?random=3',  # Fashion 3
            'https://picsum.photos/800/1000?random=4',  # Fashion 4
            'https://picsum.photos/800/1000?random=5',  # Fashion 5
            'https://picsum.photos/800/1000?random=6',  # Fashion 6
            'https://picsum.photos/800/1000?random=7',  # Fashion 7
            'https://picsum.photos/800/1000?random=8',  # Fashion 8
            'https://picsum.photos/800/1000?random=9',  # Fashion 9
            'https://picsum.photos/800/1000?random=10', # Fashion 10
        ]

        # Create media directory if it doesn't exist
        media_dir = os.path.join(settings.MEDIA_ROOT, 'products')
        os.makedirs(media_dir, exist_ok=True)

        products = Product.objects.all()
        total_products = products.count()
        
        if total_products == 0:
            self.stdout.write(self.style.WARNING('No products found. Please add some products first.'))
            return

        self.stdout.write(f'Adding demo images to {total_products} products...')
        
        updated_count = 0
        for i, product in enumerate(products):
            if not product.image:  # Only add image if the product doesn't have one
                try:
                    # Cycle through the image URLs
                    image_url = image_urls[i % len(image_urls)]
                    
                    # Download the image with a timeout and user-agent header
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                    }
                    response = requests.get(image_url, headers=headers, stream=True, timeout=10)
                    response.raise_for_status()
                    
                    # Get the image filename from the URL
                    image_name = f"product_{product.id}_{i}.jpg"
                    
                    # Save the image to the product
                    product.image.save(
                        image_name,
                        ContentFile(response.content),
                        save=True
                    )
                    
                    updated_count += 1
                    self.stdout.write(self.style.SUCCESS(f'Added image to {product.name}'))
                    
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error adding image to {product.name}: {str(e)}'))
            else:
                self.stdout.write(self.style.WARNING(f'Skipping {product.name} - already has an image'))
        
        self.stdout.write(self.style.SUCCESS(f'Successfully added demo images to {updated_count} products'))
