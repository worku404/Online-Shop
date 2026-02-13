from decimal import Decimal

import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from orders.models import Order

# create the stripe instance
stripe.api_key = settings.STRIPE_SECRET_KEY
# stripe.api_version = settings.STRIPE_API_VERSION


def payment_process(request):
    order_id = request.session.get('order_id')
    if not order_id:
        return redirect('cart:cart_detail')

    order = get_object_or_404(Order, id=order_id)
    order_items = list(order.items.select_related('product'))
    if not order_items:
        request.session.pop('order_id', None)
        return redirect('cart:cart_detail')

    if request.method == 'POST':
        success_url = request.build_absolute_uri(reverse('payment:completed'))
        cancel_url = request.build_absolute_uri(reverse('payment:canceled'))

        # stripe checkout session data
        session_data = {
            'mode': 'payment',
            'client_reference_id': order.id,
            'success_url': success_url,
            'cancel_url': cancel_url,
            'line_items': [],
        }

        # add order items to the stripe checkout session
        for item in order_items:
            session_data['line_items'].append(
                {
                    'price_data': {
                        'unit_amount': int(item.price * Decimal('100')),
                        'currency': 'usd',
                        'product_data': {
                            'name': item.product.name,
                        },
                    },
                    'quantity': item.quantity,
                }
            )

        # add shipping only when it has a charge
        if order.shipping_cost > 0:
            session_data['line_items'].append(
                {
                    'price_data': {
                        'unit_amount': int(order.shipping_cost * Decimal('100')),
                        'currency': 'usd',
                        'product_data': {
                            'name': 'Shipping',
                        },
                    },
                    'quantity': 1,
                }
            )

        # Stripe payment mode requires at least one line item.
        if not session_data['line_items']:
            return redirect('cart:cart_detail')

        if order.coupon:
            stripe_coupon = stripe.Coupon.create(
                name=order.coupon.code,
                percent_off=order.discount,
                duration='once',
            )
            session_data['discounts'] = [{'coupon': stripe_coupon.id}]

        # create stripe checkout session
        session = stripe.checkout.Session.create(**session_data)
        # redirect to stripe payment form
        return redirect(session.url, code=303)

    return render(request, 'payment/process.html', {'order': order})


# view for payment success and cancel
def payment_completed(request):
    return render(request, 'payment/completed.html')


def payment_canceled(request):
    return render(request, 'payment/canceled.html')
