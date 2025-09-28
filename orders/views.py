from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
from django.urls import reverse

def order_create(request):
    cart = Cart(request)
    if len(cart) == 0:
        return redirect('products:product_list')
        
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.save()
            
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity'],
                    is_preorder=item['product'].is_preorder
                )
            
            # Clear the cart
            cart.clear()
            
            return render(request, 'orders/order_created.html', {'order': order})
    else:
        # Pre-fill the form with user data if authenticated
        initial_data = {}
        if request.user.is_authenticated:
            initial_data = {
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email
            }
            
            # If user has a profile with address info, use it
            if hasattr(request.user, 'profile'):
                profile = request.user.profile
                if profile.address:
                    initial_data['address'] = profile.address
                if profile.city:
                    initial_data['city'] = profile.city
                if profile.postal_code:
                    initial_data['postal_code'] = profile.postal_code
                    
        form = OrderCreateForm(initial=initial_data)
    
    return render(request, 'orders/order_create.html', {'cart': cart, 'form': form})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_history.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})