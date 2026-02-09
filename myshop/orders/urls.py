from django.urls import path
"""
Defines URL routing for the 'orders' app, providing the endpoint for order creation
by mapping the 'create/' path to the order_create view.
"""
from . import views

app_name = 'orders'
urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path(
        'admin/order/<int:order_id>/',
        views.admin_order_detail,
        name='admin_order_detail'
    ),
]
