"""
Stripe Webhook handler.
Listens for asynchronous notifications from Stripe to update order status 
and trigger post-payment workflow tasks.
"""

import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Local application imports
from orders.models import Order
from .tasks import payment_completed
from shop.models import Product
from shop.recommender import Recommender

# ==============================================================================
# WEBHOOK HANDLER
# ==============================================================================

@csrf_exempt
def stripe_webhook(request):
    """
    Receiver for Stripe webhook events.
    Verifies the payload signature and updates orders upon successful payment.
    """
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    event = None
    
    # 1. Verify the webhook signature to ensure the request is from Stripe
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return HttpResponse(status=400)

    # 2. Process specific event types
    if event.type == 'checkout.session.completed':
        session = event.data.object
        
        # Verify that the session completed with a successful payment
        if (
            session.mode == 'payment' and 
            session.payment_status == 'paid'
        ):
            try:
                # Retrieve the order using the reference ID passed to Stripe
                order = Order.objects.get(
                    id=session.client_reference_id
                )
            except Order.DoesNotExist:
                return HttpResponse(status=404)
            
            # 3. Mark the order as paid and store the Stripe Payment Intent ID
            order.paid = True
            order.stripe_id = session.payment_intent
            order.save()
            
            # save items bought for product recommendations
            product_ids = order.items.values_list('product_id', flat=True)
            products = Product.objects.filter(id__in=product_ids)
            r = Recommender()
            r.product_bought(products)

                # 4. Launch asynchronous task to send invoice email/generate PDF
            payment_completed.delay(order.id)
                
    # Return 200 OK to Stripe to acknowledge receipt
    return HttpResponse(status=200)
