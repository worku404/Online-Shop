
"""
URL routing for the shop application.
Handles product listing, category filtering, and product detail views.
"""

from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    # --------------------------------------------------------------------------
    # PRODUCT CATALOG ROUTES
    # --------------------------------------------------------------------------
    
    # Root catalog view (lists all available products)
    path('', views.product_list, name='product_list'),
    
    # Filtered catalog view (lists products within a specific category)
    path(
        '<slug:category_slug>/', 
        views.product_list, 
        name='product_list_by_category'
    ),
    
    # Detailed view for a single product
    path(
        '<int:id>/<slug:slug>/', 
        views.product_detail, 
        name='product_detail'
    ),
]