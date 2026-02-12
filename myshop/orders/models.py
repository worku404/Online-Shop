"""
Models for the orders application.
Defines the Order and OrderItem structures to manage customer purchases.
"""
from decimal import Decimal
from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _

from coupons.models import Coupon

# ==============================================================================
# ORDER MODEL
# ==============================================================================

class Order(models.Model):
    """
    Stores customer information and the overall status of an order.
    """
    first_name = models.CharField(_('first_name'),max_length=50)
    last_name = models.CharField(_('last_name'),max_length=50)
    email = models.EmailField(_('e-mail'),)
    address = models.CharField(_('address'),max_length=250)
    postal_code = models.CharField(_('postal_code'),max_length=20)
    city = models.CharField(_('city'),max_length=100)
    
    # Timestamps
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    # Payment status
    paid = models.BooleanField(default=False)
    stripe_id = models.CharField(max_length=250, blank=True)
    
    coupon = models.ForeignKey(
        Coupon,
        related_name='orders',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    discount = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost(self):
        """
        Calculates the total cost of the order (sum of all items).
        """
        total_cost = self.get_total_cost_before_discount()
        return total_cost - self.get_discount()
    
    def get_total_cost_before_discount(self):
        return sum(item.get_cost() for item in self.items.all())
    
    def get_discount(self):
        total_cost = self.get_total_cost_before_discount()
        if self.discount:
            return total_cost * (self.discount/Decimal(100))
        return Decimal(0)

    def get_stripe_url(self):
        """
        Returns the Stripe dashboard URL for this order's payment.
        Handles both test and live environment paths.
        """
        if not self.stripe_id:
            return ''
        
        # Determine if we are using test or live Stripe dashboard path
        path = '/test/' if 'test' in settings.STRIPE_SECRET_KEY else '/'
        return f'https://dashboard.stripe.com{path}payments/{self.stripe_id}'


# ==============================================================================
# ORDER ITEM MODEL
# ==============================================================================

class OrderItem(models.Model):
    """
    Stores specific product details for a given order (Line items).
    """
    order = models.ForeignKey(
        Order,
        related_name='items',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        'shop.Product',
        related_name='order_items',
        on_delete=models.CASCADE
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        """
        Calculates the cost of this specific line item.
        """
        return self.price * self.quantity
    
            
