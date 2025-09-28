from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from products.models import Category
from .models import Page, ContactSubmission

class PageModelTest(TestCase):
    def setUp(self):
        self.page = Page.objects.create(
            title='Test Page',
            slug='test-page',
            content='<p>This is a test page content</p>',
            is_active=True
        )
    
    def test_page_creation(self):
        self.assertEqual(str(self.page), 'Test Page')
        self.assertEqual(self.page.slug, 'test-page')
        self.assertTrue(self.page.is_active)
        self.assertIn('test-page', self.page.get_absolute_url())

class ContactSubmissionModelTest(TestCase):
    def setUp(self):
        self.submission = ContactSubmission.objects.create(
            name='John Doe',
            email='john@example.com',
            subject='Test Subject',
            message='This is a test message',
            is_read=False
        )
    
    def test_contact_submission_creation(self):
        self.assertEqual(str(self.submission), 'Test Subject - John Doe')
        self.assertEqual(self.submission.email, 'john@example.com')
        self.assertFalse(self.submission.is_read)

class PageViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        
        # Create test pages with unique slugs to avoid conflicts
        try:
            self.page = Page.objects.create(
                title='About Us Test',
                slug='about-us-test-123',  # Use a very unique slug for testing
                content='<h1>About Us Test</h1><p>Test content</p>',
                is_active=True
            )
        except Exception as e:
            # If creation fails due to unique constraint, try with an even more unique slug
            self.page = Page.objects.create(
                title='About Us Test',
                slug=f'about-us-test-{id(self)}',  # Use object id to ensure uniqueness
                content='<h1>About Us Test</h1><p>Test content</p>',
                is_active=True
            )
        
        # Create the contact page for the contact view test
        try:
            self.contact_page = Page.objects.create(
                title='Contact Us',
                slug='contact-test-123',
                content='<h2>Get in Touch</h2><p>Test contact content</p>',
                is_active=True
            )
        except Exception as e:
            self.contact_page = Page.objects.create(
                title='Contact Us',
                slug=f'contact-test-{id(self)}',
                content='<h2>Get in Touch</h2><p>Test contact content</p>',
                is_active=True
            )
        
        # Create a category for the navigation
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )
    
    def test_about_view(self):
        response = self.client.get(reverse('pages:about'))
        self.assertEqual(response.status_code, 200)
        # Check for content from the about view
        self.assertContains(response, 'About Us')  # Content from the default about page
        self.assertContains(response, 'Test Category')  # Category in navigation
    
    def test_contact_view_get(self):
        response = self.client.get(reverse('pages:contact'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Contact Us')
        self.assertContains(response, 'Test Category')
    
    def test_contact_view_post_valid(self):
        data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'subject': 'Test Subject',
            'message': 'This is a test message'
        }
        response = self.client.post(reverse('pages:contact'), data)
        
        # Should redirect to success URL
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('pages:contact'))
        
        # Check if the submission was created
        self.assertEqual(ContactSubmission.objects.count(), 1)
        submission = ContactSubmission.objects.first()
        self.assertEqual(submission.name, 'Test User')
        self.assertEqual(submission.email, 'test@example.com')
    
    def test_contact_view_post_invalid(self):
        data = {
            'name': '',  # Missing name
            'email': 'invalid-email',  # Invalid email
            'subject': '',  # Missing subject
            'message': ''  # Missing message
        }
        response = self.client.post(reverse('pages:contact'), data)
        
        # Should return to the form with errors
        self.assertEqual(response.status_code, 200)
        # Check that form has errors by checking for Django's error indicators
        self.assertContains(response, 'invalid-feedback')  # Django Bootstrap error class
    
    def test_page_detail_view(self):
        # Use the slug from the created page
        response = self.client.get(reverse('pages:page_detail', args=[self.page.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'About Us Test')
        self.assertContains(response, 'Test Category')
    
    def test_inactive_page(self):
        # Create an inactive page
        inactive_page = Page.objects.create(
            title='Inactive Page',
            slug='inactive-page',
            content='This page should not be visible',
            is_active=False
        )
        
        # Should return 404 for inactive pages
        response = self.client.get(reverse('pages:page_detail', args=['inactive-page']))
        self.assertEqual(response.status_code, 404)
