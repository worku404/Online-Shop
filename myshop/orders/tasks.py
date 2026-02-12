"""
Asynchronous tasks for the orders application.
Handles background processes like sending confirmation emails.
"""

from celery import shared_task

# Django imports
from django.core.mail import send_mail

# Local imports
from .models import Order

# ==============================================================================
# ASYNCHRONOUS TASKS
# ==============================================================================

@shared_task
def order_created(order_id):
    """
    Task to send an email notification when an order is successfully created.
    """
    # 1. Retrieve order details
    order = Order.objects.get(id=order_id)
    
    # 2. Compose the email
    subject = f'Order nr. {order_id}'
    message = (
        f'Dear {order.first_name},\n\n'
        f'You have successfully placed an order. '
        f'Your order ID is {order.id}.'
    )
    
    # 3. Send the email
    mail_sent = send_mail(
        subject,
        message,
        'admin@myshop.com',
        [order.email]
    )
    
    return mail_sent