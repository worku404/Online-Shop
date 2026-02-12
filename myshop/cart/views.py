"""
Views for the shopping cart application.
Handles adding, removing, and viewing items in the cart.
"""

# Django imports
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

# Project imports
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from coupons.forms import CouponApplyForm
from shop.recommender import Recommender
# ==============================================================================
# CART MANAGEMENT VIEWS
# ==============================================================================

@require_POST
def cart_add(request, product_id):
    """
    View to add a product to the cart or update its quantity.
    Requires a POST request containing the CartAddProductForm data.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(
            product=product,
            quantity=cd['quantity'],
            override_quantity=cd['override']
        )
    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, product_id):
    """
    View to remove a specific product from the cart.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product=product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    """
    Displays the current contents of the shopping cart.
    Constructs update forms for each item to allow quantity changes.
    """
    cart = Cart(request)
    
    # Initialize quantity update forms for each item in the cart
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={
                'quantity': item['quantity'],
                'override': True
            }
        )

    coupon_apply_form = CouponApplyForm()      
    r = Recommender()
    cart_products = [item['product'] for item in cart if 'product' in item]
    if (cart_products):
        recommended_products = r.suggest_products_for(cart_products, max_results=4) 
    else:
        recommended_products =[]
    return render(
        request,
        'cart/detail.html',
        {'cart': cart,
         'coupon_apply_form': coupon_apply_form,
         'recommended_products':recommended_products
         }
    )
