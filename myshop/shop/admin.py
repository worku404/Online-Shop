from django.contrib import admin

# Register your models here.
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    
@admin.register(Product)
class ProductAdim(admin.ModelAdmin):
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
    prepopulated_fields = {'slug': ('name',)}
    

"""
This is a Django admin class for the Product model, registered with the admin site.
It customizes the admin interface for managing products in the online shop.

- list_display: Shows these fields in the admin list view (name, slug, price, availability, creation and update dates).
- list_filter: Allows filtering products by availability, creation date, and update date.
- list_editable: Lets you edit price and availability directly from the list view.
- prepopulated_fields: Automatically fills the slug field based on the name field.

This makes it easy to view, filter, and edit product details in the Django admin panel.
"""