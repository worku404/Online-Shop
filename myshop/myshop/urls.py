"""
Root URL configuration for the myshop project.
Routes requests to individual app URL modules and handles media serving in development.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

# ==============================================================================
# URL ROUTING
# ==============================================================================

urlpatterns = [
    # Django Administration
    path('admin/', admin.site.urls),
    
    # Shopping Cart
    path('cart/', include('cart.urls', namespace='cart')),
    
    # Order Processing
    path('orders/', include('orders.urls', namespace='orders')),
    
    # Payment Integration (Stripe)
    path('payment/', include('payment.urls', namespace='payment')),
    
    # coupon for discount
    path('coupons/', include('coupons.urls', namespace='coupons')),
    
    # Product Catalog (Root)
    path('', include('shop.urls', namespace='shop')),
]

# ==============================================================================
# MEDIA SERVING (DEVELOPMENT ONLY)
# ==============================================================================

if settings.DEBUG:
    # Append patterns to serve media files manually during development
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )