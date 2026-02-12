from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Coupon(models.Model):
    """
    Coupon model representing a percentage discount valid for a time window.
    Fields:
      - code: unique coupon identifier
      - valid_from / valid_to: validity period
      - discount: integer percent (0-100)
      - active: whether coupon is usable
    """
    code = models.CharField(max_length=50, unique=True)
    valid_from = models.DateTimeField(help_text='Start datetime for coupon validity')
    valid_to = models.DateTimeField(help_text='End datetime for coupon validity')
    discount = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text='Percentage value (0 to 100)'
    )
    active = models.BooleanField(default=True, help_text='Is the coupon active?')

    def __str__(self) -> str:
        return self.code