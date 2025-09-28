from django.apps import AppConfig
from django.db.models.signals import post_migrate

def create_default_pages(sender, **kwargs):
    from .models import Page
    
    # Create default About page if it doesn't exist
    about_page, created = Page.objects.get_or_create(
        slug='about',
        defaults={
            'title': 'About Us',
            'content': '''<h2>Our Story</h2>
            <p>Welcome to HK Fashion, your number one source for all things fashion. We're dedicated to giving you the very best of clothing, with a focus on quality, customer service, and uniqueness.</p>
            <p>Founded in 2023, HK Fashion has come a long way from its beginnings. When we first started out, our passion for fashion drove us to start our own business.</p>
            <h3>Our Mission</h3>
            <p>Our mission is to provide high-quality, fashionable clothing at affordable prices while ensuring a seamless shopping experience for our customers.</p>
            <h3>Why Choose Us?</h3>
            <ul>
                <li>High-quality products</li>
                <li>Affordable prices</li>
                <li>Fast shipping</li>
                <li>Excellent customer service</li>
            </ul>''',
            'is_active': True
        }
    )
    
    # Create default Contact page if it doesn't exist
    contact_page, created = Page.objects.get_or_create(
        slug='contact',
        defaults={
            'title': 'Contact Us',
            'content': '''<h2>Get in Touch</h2>
            <p>We'd love to hear from you! Please fill out the form below and we'll get back to you as soon as possible.</p>
            <div class="contact-info">
                <p><i class="fas fa-map-marker-alt"></i> 123 Fashion Street, Dhaka 1212, Bangladesh</p>
                <p><i class="fas fa-phone"></i> +880 1234 567890</p>
                <p><i class="fas fa-envelope"></i> info@hkfashion.com</p>
            </div>''',
            'is_active': True
        }
    )
    
    # Create default Blog page
    blog_page, created = Page.objects.get_or_create(
        slug='blog',
        defaults={
            'title': 'Blog',
            'content': '''<h2>Latest Fashion News & Trends</h2>
            <p>Check back soon for our latest blog posts about fashion trends, styling tips, and more!</p>''',
            'is_active': True
        }
    )
    
    # Create default FAQs page
    faqs_page, created = Page.objects.get_or_create(
        slug='faqs',
        defaults={
            'title': 'Frequently Asked Questions',
            'content': '''<h2>Frequently Asked Questions</h2>
            <div class="accordion" id="faqAccordion">
                <div class="accordion-item">
                    <h3 class="accordion-header" id="headingOne">
                        <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapseOne" aria-expanded="true" aria-controls="collapseOne">
                            What payment methods do you accept?
                        </button>
                    </h3>
                    <div id="collapseOne" class="accordion-collapse collapse show" aria-labelledby="headingOne" data-bs-parent="#faqAccordion">
                        <div class="accordion-body">
                            We accept all major credit cards, PayPal, and bank transfers.
                        </div>
                    </div>
                </div>
                <div class="accordion-item">
                    <h3 class="accordion-header" id="headingTwo">
                        <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseTwo" aria-expanded="false" aria-controls="collapseTwo">
                            What is your return policy?
                        </button>
                    </h3>
                    <div id="collapseTwo" class="accordion-collapse collapse" aria-labelledby="headingTwo" data-bs-parent="#faqAccordion">
                        <div class="accordion-body">
                            We offer a 30-day return policy for all unused and unwashed items with original tags attached.
                        </div>
                    </div>
                </div>
                <div class="accordion-item">
                    <h3 class="accordion-header" id="headingThree">
                        <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseThree" aria-expanded="false" aria-controls="collapseThree">
                            How long does shipping take?
                        </button>
                    </h3>
                    <div id="collapseThree" class="accordion-collapse collapse" aria-labelledby="headingThree" data-bs-parent="#faqAccordion">
                        <div class="accordion-body">
                            Standard shipping typically takes 3-5 business days. Express shipping options are available at checkout.
                        </div>
                    </div>
                </div>
            </div>''',
            'is_active': True
        }
    )
    
    # Create default Privacy Policy page
    privacy_policy_page, created = Page.objects.get_or_create(
        slug='privacy-policy',
        defaults={
            'title': 'Privacy Policy',
            'content': '''<h2>Privacy Policy</h2>
            <p>Last updated: {% now "F j, Y" %}</p>
            
            <h3>1. Information We Collect</h3>
            <p>We collect information that you provide directly to us, such as when you create an account, place an order, or contact us.</p>
            
            <h3>2. How We Use Your Information</h3>
            <p>We use the information we collect to provide, maintain, and improve our services, process transactions, and communicate with you.</p>
            
            <h3>3. Information Sharing</h3>
            <p>We do not sell or share your personal information with third parties except as described in this policy.</p>
            
            <h3>4. Security</h3>
            <p>We take reasonable measures to help protect your personal information from loss, theft, misuse, and unauthorized access.</p>
            
            <h3>5. Changes to This Policy</h3>
            <p>We may update this privacy policy from time to time. We will notify you of any changes by posting the new policy on this page.</p>''',
            'is_active': True
        }
    )
    
    # Create default Terms & Conditions page
    terms_page, created = Page.objects.get_or_create(
        slug='terms-conditions',
        defaults={
            'title': 'Terms & Conditions',
            'content': '''<h2>Terms & Conditions</h2>
            <p>Last updated: {% now "F j, Y" %}</p>
            
            <h3>1. General Terms</h3>
            <p>By accessing and using this website, you accept and agree to be bound by these terms and conditions.</p>
            
            <h3>2. Products and Pricing</h3>
            <p>We reserve the right to change prices and availability of products at any time without notice.</p>
            
            <h3>3. Orders and Payment</h3>
            <p>All orders are subject to acceptance and availability. Payment must be received before we can process your order.</p>
            
            <h3>4. Returns and Refunds</h3>
            <p>Please refer to our Returns Policy for information about returning products and requesting refunds.</p>
            
            <h3>5. Intellectual Property</h3>
            <p>All content on this website, including text, graphics, logos, and images, is our property and is protected by copyright laws.</p>''',
            'is_active': True
        }
    )
    
    # Create default Shipping & Returns page
    shipping_returns_page, created = Page.objects.get_or_create(
        slug='shipping-returns',
        defaults={
            'title': 'Shipping & Returns',
            'content': '''<h2>Shipping & Returns</h2>
            
            <h3>Shipping Information</h3>
            <p>We offer worldwide shipping. Shipping costs and delivery times vary depending on your location and the shipping method selected at checkout.</p>
            
            <h4>Standard Shipping</h4>
            <ul>
                <li>3-5 business days for domestic orders</li>
                <li>7-14 business days for international orders</li>
                <li>Tracking information provided for all orders</li>
            </ul>
            
            <h4>Express Shipping</h4>
            <ul>
                <li>1-2 business days for domestic orders</li>
                <li>3-5 business days for international orders</li>
                <li>Priority processing and delivery</li>
            </ul>
            
            <h3>Returns & Exchanges</h3>
            <p>We want you to be completely satisfied with your purchase. If for any reason you're not satisfied, we're here to help.</p>
            
            <h4>Return Policy</h4>
            <ul>
                <li>30-day return policy from the date of delivery</li>
                <li>Items must be unused, unworn, and in original condition with tags attached</li>
                <li>Original proof of purchase required</li>
                <li>Final sale items are not eligible for return or exchange</li>
            </ul>
            
            <h4>How to Return</h4>
            <ol>
                <li>Contact our customer service team to initiate a return</li>
                <li>Pack the item(s) securely in the original packaging</li>
                <li>Include the return form with your package</li>
                <li>Ship the package to the provided return address</li>
            </ol>
            
            <h4>Refunds</h4>
            <p>Refunds will be processed within 3-5 business days after we receive your return. The refund will be issued to the original payment method.</p>''',
            'is_active': True
        }
    )

class PagesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pages'
    
    def ready(self):
        # Connect the create_default_pages function to the post_migrate signal
        post_migrate.connect(create_default_pages, sender=self)
