from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = 'pages'

urlpatterns = [
    # Specific page views
    path('about/', views.about, name='about'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    
    # Dynamic page view (must come after specific views)
    path('<slug:slug>/', views.PageDetailView.as_view(), name='page_detail'),
    
    # Redirects for backward compatibility
    path('pages/about/', RedirectView.as_view(pattern_name='pages:about', permanent=True)),
    path('pages/contact/', RedirectView.as_view(pattern_name='pages:contact', permanent=True)),
]
