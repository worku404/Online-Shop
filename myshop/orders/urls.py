"""
URL routing for the orders application.
Handles the checkout process and staff-only administrative views for orders.
"""
from django.utils.translation import gettext_lazy as _
from django.urls import path
from . import views
app_name = 'orders'

urlpatterns = [
    # --------------------------------------------------------------------------
    # PUBLIC ROUTES
    # --------------------------------------------------------------------------
    # Endpoint to handle order creation (checkout process)
    path(_('create/'), views.order_create, name='order_create'),

    # --------------------------------------------------------------------------
    # ADMIN / STAFF ROUTES
    # --------------------------------------------------------------------------
    # Custom detailed view for an order within the admin site
    path(
        'admin/order/<int:order_id>/',
        views.admin_order_detail,
        name='admin_order_detail'
    ),
    
    # Endpoint to generate and download a PDF invoice for an order
    path(
        'admin/order/<int:order_id>/pdf/',
        views.admin_order_pdf,
        name='admin_order_pdf'
    ),
]