from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Category, Product
from cart.forms import CartAddProductForm

def home_view(request):
    """View for the home page"""
    products = Product.objects.filter(available=True)[:8]  # Get the first 8 available products
    return render(request, 'home.html', {'products': products})

def product_list(request, category_slug=None):
    """View for listing products with search and category filtering"""
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    query = request.GET.get('q', '').strip()
    
    # Apply search query if provided
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )
    
    # Apply category filter if provided
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    # Get sort parameter
    sort_by = request.GET.get('sort', 'name')
    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    elif sort_by == 'newest':
        products = products.order_by('-created')
    else:  # Default sort by name
        products = products.order_by('name')
    
    # Pagination
    paginator = Paginator(products, 12)  # Show 12 products per page
    page = request.GET.get('page')
    
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        products = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results
        products = paginator.page(paginator.num_pages)
    
    return render(request, 'products/product_list.html',
                 {'category': category,
                  'categories': categories,
                  'products': products,
                  'query': query,
                  'sort_by': sort_by})

def product_detail(request, id, slug):
    """View for displaying product details"""
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    
    return render(request, 'products/product_detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form})