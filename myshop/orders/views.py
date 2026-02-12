"""
Order management views.
Handles order creation, admin details, and PDF invoice generation.
"""

# Django imports
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.template.loader import render_to_string
from django.contrib.staticfiles import finders
from django.http import HttpResponse

# Third-party imports
import weasyprint

# Local app imports
from .forms import OrderCreateForm
from .models import OrderItem, Order
from .tasks import order_created
from cart.cart import Cart


# ==============================================================================
# PUBLIC VIEWS
# ==============================================================================

def order_create(request):
    """
    Handles the checkout process. 
    Saves order details, creates line items, and clears the cart.
    """
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            # 1. Save the initial order and apply discount
            order = form.save(commit=False)
            
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            
            # 2. Create OrderItem instances for each product in the cart
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
                
            # 3. Clear the session cart
            cart.clear()

            # 4. Launch asynchronous task to send confirmation email
            order_created.delay(order.id)

            # 5. Set order ID in session and redirect to payment processing
            request.session['order_id'] = order.id
            return redirect('payment:process')
    else:
        form = OrderCreateForm()
        
    return render(
        request,
        'orders/order/create.html',
        {
            'cart': cart,
            'form': form
        }
    )


# ==============================================================================
# ADMIN & STAFF VIEWS
# ==============================================================================

@staff_member_required
def admin_order_detail(request, order_id):
    """
    Displays the detailed view of an order for staff members only.
    """
    order = get_object_or_404(Order, id=order_id)
    return render(
        request,
        'admin/orders/order/detail.html', 
        {'order': order}
    )


@staff_member_required
def admin_order_pdf(request, order_id):
    """
    Generates and returns a PDF invoice for a specific order.
    Utilizes WeasyPrint for HTML-to-PDF conversion.
    """
    order = get_object_or_404(Order, id=order_id)
    
    # Render the PDF template to a string
    html = render_to_string('orders/order/pdf.html', {'order': order})
    
    # Prepare HTTP response with PDF content type
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
    
    # Generate PDF from HTML and write to response
    weasyprint.HTML(string=html).write_pdf(
        response,
        stylesheets=[weasyprint.CSS(finders.find('shop/css/pdf.css'))]
    )
    
    return response