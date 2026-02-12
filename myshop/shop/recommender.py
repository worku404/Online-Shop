from django.conf import settings
import redis

from .models import Product


# ============================================================
# Redis Connection
# ============================================================
# Single Redis client used by the recommender to store and read
# product co-purchase scores.
r = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
)


class Recommender:
    # ========================================================
    # Key Builder
    # ========================================================
    def get_product_key(self, id):
        """
        Return the Redis sorted-set key for a product.
        Each key stores products that were purchased together with it.
        """
        return f"product: {id}:purchased_with"

    # ========================================================
    # Write Flow: Store Co-Purchase Data
    # ========================================================
    def product_bought(self, products):
        """
        For each product in the given list, increase score for every
        other product bought in the same order.
        """
        product_ids = [p.id for p in products]

        for product_id in product_ids:
            for with_id in product_ids:
                # Skip same product (no self-pairing)
                if product_id != with_id:
                    # Increment co-purchase score in Redis sorted set
                    r.zincrby(self.get_product_key(product_id), 1, with_id)

    # ========================================================
    # Read Flow: Suggest Products
    # ========================================================
    def suggest_products_for(self, products, max_results=6):
        """
        Return product recommendations ordered by Redis score.
        """
        product_ids = [p.id for p in products]

        if len(products)==1:
            # Current logic path for non-empty input:
            # use recommendations from the first product key.
            suggestions = r.zrange(
                self.get_product_key(product_ids[0]),
                0,
                -1,
                desc=True,
            )[:max_results]
        else:
            # Current logic path for empty input:
            # combine sorted sets into a temporary key.
            flat_ids = "".join([str(id) for id in product_ids])
            tmp_key = f"tmp_{flat_ids}"

            # Merge scores from all selected product keys
            keys = [self.get_product_key(id) for id in product_ids]
            r.zunionstore(tmp_key, keys)

            # Remove products already in input from recommendations
            r.zrem(tmp_key, *product_ids)

            # Read top products by descending score
            suggestions = r.zrange(tmp_key, 0, -1, desc=True)[:max_results]

            # Clean up temporary key
            r.delete(tmp_key)

        # Convert Redis values to integer product IDs
        suggested_products_ids = [int(id) for id in suggestions]

        # Fetch products from DB and preserve Redis ranking order
        suggested_products = list(
            Product.objects.filter(id__in=suggested_products_ids)
        )
        suggested_products.sort(
            key=lambda x: suggested_products_ids.index(x.id)
        )

        return suggested_products

    # ========================================================
    # Maintenance: Clear Stored Co-Purchase Data
    # ========================================================
    def clear_purchases(self):
        """
        Remove all stored recommendation data from Redis.
        """
        for id in Product.objects.values_list("id", flat=True):
            r.delete(self.get_product_key(id))
