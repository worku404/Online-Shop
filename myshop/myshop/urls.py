"""
Root URL configuration for the myshop project.
Routes requests to individual app URL modules and handles media serving in development.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _
from payment import webhooks

# ==============================================================================
# URL ROUTING
# ==============================================================================

urlpatterns = i18n_patterns(
    # Django Administration
    path('admin/', admin.site.urls),
    
    # Shopping Cart
    path(_('cart/'), include('cart.urls', namespace='cart')),
    
    # Order Processing
    path(_('orders/'), include('orders.urls', namespace='orders')),
    
    # Payment Integration (Stripe)
    path(_('payment/'), include('payment.urls', namespace='payment')),
    
    # coupon for discount
    path(_('coupons/'), include('coupons.urls', namespace='coupons')),
    
    path('rosetta/', include('rosetta.urls')),
    # Product Catalog (Root)
    path('', include('shop.urls', namespace='shop')),
)

urlpatterns +=[
    path('payment/webhook/', webhooks.stripe_webhook, name='stripe_webhook'),
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