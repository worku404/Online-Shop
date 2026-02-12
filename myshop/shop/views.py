"""
Views for the shop application.
Handles product catalog listing and individual product details.
"""

# Django imports
from django.shortcuts import render, get_object_or_404

# Local app imports
from .models import Product, Category
from cart.forms import CartAddProductForm
from .recommender import Recommender

# ==============================================================================
# CATALOG VIEWS
# ==============================================================================

def product_list(request, category_slug=None):
    """
    Lists all available products or filters them by a specific category.
    """
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    
    if category_slug:
        language = request.LANGUAGE_CODE
        # Use DOUBLE underscores (__) here:
        category = get_object_or_404(Category,
                                     translations__language_code=language,
                                     translations__slug=category_slug)
        products = products.filter(category=category)
        
    return render(
        request,
        'shop/product/list.html',
        {
            'category': category,
            'categories': categories,
            'products': products
        }
    )


def product_detail(request, id, slug):
    """
    Displays the detailed page for a specific product.
    Includes the form to add the product to the shopping cart.
    """
    language = request.LANGUAGE_CODE
    product = get_object_or_404(Product,
                                id=id,
                                translations__language_code=language,
                                translations__slug=slug,
                                available=True)
    
    # Form to select quantity and add to cart
    cart_product_form = CartAddProductForm()
    r = Recommender()
    recommender_products = r.suggest_products_for([product], 4)
    
    return render(
        request, 
        'shop/product/detail.html',
        {
            'product': product,
            'cart_product_form': cart_product_form,
            'recommended_products': recommender_products
        }
    )