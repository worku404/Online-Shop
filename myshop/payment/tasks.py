"""
Asynchronous tasks for the payment application.
Handles post-payment actions like generating invoices and sending emails.
"""

from io import BytesIO
import weasyprint
from celery import shared_task

# Django imports
from django.contrib.staticfiles import finders
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

# Local imports
from orders.models import Order

@shared_task
def payment_completed(order_id):
    """
    Task to send an e-mail notification with a PDF invoice 
    when an order is successfully paid.
    """
    # 1. Retrieve the order object
    order = Order.objects.get(id=order_id)
    
    # 2. Initialize the email message
    subject = f'My shop - Invoice no. {order.id}'
    message = 'Please find attached the invoice for your recent purchase.'
    email = EmailMessage(
        subject,
        message,
        'admin@myshop.com',
        [order.email]
    )
    
    # 3. Generate the PDF invoice
    # Render the HTML template with order data
    html = render_to_string('orders/order/pdf.html', {'order': order})
    out = BytesIO()
    
    # Locate the CSS file for styling the PDF
    stylesheets = [weasyprint.CSS(finders.find('shop/css/pdf.css'))]
    
    # Convert HTML string to a PDF file in memory (BytesIO)
    weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)
    
    # 4. Attach the generated PDF to the email
    email.attach(
        f'order_{order.id}.pdf',
        out.getvalue(),
        'application/pdf'
    )
    
    # 5. Send the email
    email.send()