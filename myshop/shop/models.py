"""
Models for the shop application.
Defines Category and Product structures for the product catalog.
"""

from django.db import models
from django.urls import reverse

from parler.models import TranslatableModel, TranslatedFields
# ==============================================================================
# CATEGORY MODEL
# ==============================================================================

class Category(TranslatableModel):
    
    """
    Groups products into logical classifications.
    """
    translations = TranslatedFields(
        name = models.CharField(max_length=200),
        slug = models.SlugField(max_length=200, unique=True),
    )
    class Meta:
        # ordering = ['name']
        # indexes = [
        #     models.Index(fields=['name']),
        # ]
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self) -> str:
        return self.name
    
    def get_absolute_url(self):
        """
        Returns the URL to list products belonging to this category.
        """
        return reverse(
            'shop:product_list_by_category',
            args=[self.slug]
        )


# ==============================================================================
# PRODUCT MODEL
# ==============================================================================

class Product(TranslatableModel):
    """
    Stores individual product details and availability status.
    """
    # Relationships
    
    category = models.ForeignKey(
        Category,
        related_name='products',
        on_delete=models.CASCADE
    )
    
    # Basic Information
    translations = TranslatedFields(
        name = models.CharField(max_length=200),
        slug = models.SlugField(max_length=200),
        description = models.TextField(blank=True),
    )
    image = models.ImageField(
        upload_to='products/%y/%m/%d',
        blank=True
    )
    
    # Financials & Status
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    
    # Timestamps
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    weight = models.PositiveIntegerField(
        help_text="weight in grams",
        default=0
    )
    
    class Meta:
        # ordering = ['name']
        indexes = [
            # models.Index(fields=['id', 'slug']),
            # models.Index(fields=['name']),
            models.Index(fields=['-created']),
        ]

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        """
        Returns the URL for the detailed view of this product.
        """
        return reverse("shop:product_detail", args=[self.id, self.slug])