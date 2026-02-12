"""
URL routing for the payment application.
Includes endpoints for Stripe checkout redirection, success/failure pages, 
and the Stripe webhook listener.
"""

from django.urls import path
from . import views, webhooks

app_name = 'payment'

urlpatterns = [
    # --------------------------------------------------------------------------
    # PAYMENT FLOW ROUTES
    # --------------------------------------------------------------------------
    
    # Entrance point to initiate the Stripe Checkout session
    path('process/', views.payment_process, name='process'),
    
    # Redirection landing page after a successful payment
    path('completed/', views.payment_completed, name='completed'),
    
    # Redirection landing page if the user cancels the payment process
    path('canceled/', views.payment_canceled, name='canceled'),

    # --------------------------------------------------------------------------
    # WEBHOOKS
    # --------------------------------------------------------------------------
    
    # Endpoint for Stripe to send asynchronous event notifications (e.g., payment success)
    path('webhook/', webhooks.stripe_webhook, name='stripe_webhook'),
]