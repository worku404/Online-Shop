"""
Admin configuration for the shop application.
Defines the management interface for categories and products.
"""

from django.contrib import admin
from .models import Category, Product

from parler.admin import TranslatableAdmin
# ==============================================================================
# CATEGORY ADMIN
# ==============================================================================

@admin.register(Category)
class CategoryAdmin(TranslatableAdmin):
    """
    Administration interface for the Category model.
    """
    list_display = ['name', 'slug']
    def get_prepopulated_fields(self, request, obj=None):
        return  {'slug': ('name',)}


# ==============================================================================
# PRODUCT ADMIN
# ==============================================================================

@admin.register(Product)
class ProductAdmin(TranslatableAdmin):
    """
    Administration interface for the Product model.
    - list_display: Fields shown in the admin list view.
    - list_filter: Sidebar filters for availability and dates.
    - list_editable: Fields that can be edited directly in the list view.
    - prepopulated_fields: Slugs generated automatically from names.
    """
    list_display = [
        'name',
        'slug',
        'price',
        'available',
        'created',
        'updated'
    ]
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available']

    def get_prepopulated_fields(self, request, obj=None):
        return  {'slug': ('name',)}