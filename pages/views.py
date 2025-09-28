from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.utils import timezone

from products.models import Category
from .models import Page, ContactSubmission
from .forms import ContactForm

class PageDetailView(DetailView):
    model = Page
    template_name = 'pages/page_detail.html'
    context_object_name = 'page'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Page.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

def about(request):
    try:
        page = Page.objects.get(slug='about', is_active=True)
    except Page.DoesNotExist:
        # Create a default about page if it doesn't exist
        page = Page.objects.create(
            title='About Us',
            slug='about',
            content='''<h2>Our Story</h2>
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
            is_active=True
        )
    
    # Get categories for the navigation
    from products.models import Category
    categories = Category.objects.all()
    
    return render(request, 'pages/page_detail.html', {
        'page': page,
        'categories': categories
    })

class ContactView(FormView):
    template_name = 'pages/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('pages:contact')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        
        # Try to get the contact page content
        try:
            context['page'] = Page.objects.get(slug='contact', is_active=True)
        except Page.DoesNotExist:
            # Create a default contact page if it doesn't exist
            context['page'] = Page.objects.create(
                title='Contact Us',
                slug='contact',
                content='''<h2>Get in Touch</h2>
                <p>We'd love to hear from you! Please fill out the form below and we'll get back to you as soon as possible.</p>
                <div class="contact-info">
                    <p><i class="fas fa-map-marker-alt"></i> 123 Fashion Street, City, Country</p>
                    <p><i class="fas fa-phone"></i> +1 234 567 890</p>
                    <p><i class="fas fa-envelope"></i> info@hkfashion.com</p>
                </div>''',
                is_active=True
            )
        
        return context

    def form_valid(self, form):
        # Save the contact submission
        ContactSubmission.objects.create(
            name=form.cleaned_data['name'],
            email=form.cleaned_data['email'],
            subject=form.cleaned_data['subject'],
            message=form.cleaned_data['message']
        )
        
        # Send email notification (you'll need to implement this)
        # send_contact_notification(form.cleaned_data)
        
        messages.success(self.request, 'Thank you for your message! We will get back to you soon.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)
