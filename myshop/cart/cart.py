"""
Shopping cart management class.
Handles session-based cart storage, item calculations, and data retrieval.
"""

from decimal import Decimal
from django.conf import settings
from shop.models import Product
from coupons.models import Coupon

# ==============================================================================
# CART CLASS
# ==============================================================================

class Cart:
    def __init__(self, request) -> None:
        """
        Initialize the cart using the session.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        
        if not cart:
            # Save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        
        # store current applied coupon
        self.coupon_id = self.session.get('coupon_id')
        
    @property
    def coupon(self):
        if self.coupon_id:
            try:
                return Coupon.objects.get(id=self.coupon_id)
            except Coupon.DoesNotExist:
                pass
        return None
    
    def get_discount(self):
        if self.coupon:
            return (
                self.coupon.discount / Decimal(100)
            ) * self.get_total_price()
        return Decimal(0)
    
    def getTotalPriceAfterDiscount(self):
        return self.get_total_price() - self.get_discount()

    # --------------------------------------------------------------------------
    # DATA MANAGEMENT
    # --------------------------------------------------------------------------

    def add(self, product, quantity=1, override_quantity=False):
        """
        Add a product to the cart or update its quantity.
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)
            }
        
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def remove(self, product):
        """
        Remove a product from the cart.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        """
        Mark the session as modified to ensure it is saved.
        """
        self.session.modified = True

    # --------------------------------------------------------------------------
    # ITERATION & CALCULATIONS
    # --------------------------------------------------------------------------

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products from the database.
        """
        product_ids = self.cart.keys()
        # Fetch actual Product objects from DB
        products = Product.objects.filter(id__in=product_ids)
        
        # Copy nested item dicts so runtime formatting (Decimal/product object)
        # doesn't leak back into session JSON payload.
        cart = {k: v.copy() for k, v in self.cart.items()}
        existing_ids = set()
        for product in products:
            product_id = str(product.id)
            cart[product_id]['product'] = product
            existing_ids.add(product_id)

        # Remove stale cart rows that reference deleted products.
        stale_ids = [product_id for product_id in list(cart.keys()) if product_id not in existing_ids]
        if stale_ids:
            for product_id in stale_ids:
                self.cart.pop(product_id, None)
                cart.pop(product_id, None)
            self.save()
             
        for item in cart.values():
            if 'product' not in item:
                continue
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Return the total total number of items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        Calculate the total cost of all items in the cart.
        """
        return sum(
            Decimal(item['price']) * item['quantity'] 
            for item in self.cart.values()
        )

    # --------------------------------------------------------------------------
    # UTILITIES
    # --------------------------------------------------------------------------

    def clear(self):
        """
        Remove the cart from the session.
        """
        del self.session[settings.CART_SESSION_ID]
        self.save()
