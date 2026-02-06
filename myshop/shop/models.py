from django.db import models
from django.urls import reverse
# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=200)
    slug=models.SlugField(max_length=200, unique=True)
    
    class Meta:
        ordering=['name']
        indexes = [
            models.Index(fields=['name']),
        ]
        verbose_name='category'
        verbose_name_plural = 'categories'
    def __str__(self) -> str:
        return self.name
    def get_absolute_url(self):
        return reverse(
            'shop:product_list_by_category',
            args=[self.slug]
        )
    
class Product (models.Model):
    category = models.ForeignKey(
        Category,
        related_name='products',
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    image = models.ImageField(
        upload_to = 'products/%y/%m/%d',
        blank=True
    )
    description = models.TextField(blank=True)
    price= models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        indexes =[
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created']),
        ]
    def __str__(self) -> str:
        return self.name
    def get_absolute_url(self):
        return reverse("shop:product_detail", args=[self.id, self.slug])

    """The Product model represents an item available for sale in an online shop. It inherits from Django's models.Model,
    allowing it to be stored in a database and interact with Django's ORM (Object-Relational Mapping) system. This model
    is designed to store essential information about products, including their categorization, naming, visual representation,
    pricing, availability, and timestamps for creation and updates. It includes database optimizations through indexing
    and ordering to improve query performance.
    Step-by-step explanation of the class components:
    1. **Inheritance from models.Model**: This makes Product a Django model, enabling database table creation, CRUD operations,
        and integration with Django's admin interface, forms, and views.
    2. **Fields**:
        - `category`: A ForeignKey field linking each product to a Category model instance. This establishes a many-to-one
            relationship where multiple products can belong to one category. The `related_name='products'` allows reverse
            lookups from Category to its products (e.g., category.products.all()). On deletion of the category, all related
            products are cascaded (deleted) due to `on_delete=models.CASCADE`.
        - `name`: A CharField for the product's name, limited to 200 characters. This is a required field (no blank=True),
            used for display and identification.
        - `slug`: A SlugField for a URL-friendly version of the name, also max 200 characters. Slugs are typically used in
            URLs for SEO and readability (e.g., 'wireless-headphones' instead of 'Wireless Headphones').
        - `image`: An ImageField for uploading product images. Files are uploaded to a dynamic path 'products/%y/%m/%d'
            (year/month/day), organizing images by date. It's optional (blank=True), so products can exist without images.
        - `description`: A TextField for detailed product descriptions. It's optional (blank=True), allowing for rich text
            or plain descriptions.
        - `price`: A DecimalField for the product's price, with up to 10 digits total and 2 decimal places (e.g., 99999999.99).
            This ensures precise monetary calculations without floating-point errors.
        - `available`: A BooleanField indicating if the product is in stock or active for sale. Defaults to True, meaning
            products are available by default.
        - `created`: A DateTimeField automatically set to the current timestamp when the product is first created
            (`auto_now_add=True`). This is immutable and tracks creation time.
        - `updated`: A DateTimeField automatically updated to the current timestamp whenever the product is saved
            (`auto_now=True`). This tracks the last modification time.
    3. **Meta Class**:
        - `ordering`: Specifies the default ordering for querysets, sorting products alphabetically by name. This affects
            how products are listed in views and admin without explicit ordering.
        - `indexes`: Defines database indexes for performance optimization:
            - `models.Index(fields=['id', 'slug'])`: Speeds up queries filtering by id and slug, useful for URL lookups.
            - `models.Index(fields=['name'])`: Optimizes searches or sorts by name.
            - `models.Index(fields=['-created'])`: Indexes the created field in descending order, efficient for queries
            like "latest products" (note the '-' for descending).
    4. **Methods**:
        - `__str__`: Returns the product's name as its string representation. This is used in Django's admin, shell,
            and anywhere the object is printed or displayed as a string, providing a human-readable identifier.
    Usage Notes:
    - This model is part of an e-commerce application, likely used in views for product listings, details, and cart functionality.
    - Ensure the Category model is defined elsewhere, as it's referenced here.
    - Image uploads require proper media settings in Django (e.g., MEDIA_URL, MEDIA_ROOT).
    - For production, consider adding validation (e.g., positive price) via clean() method or forms.
    - Indexes improve performance but increase storage; monitor database size.
    """



"""
    Django model representing a product/category taxonomy node.
    Step-by-step explanation of what this model defines and how Django uses it:
    1) Model declaration and purpose
        - This class subclasses `django.db.models.Model`, which tells Django:
          * This Python class maps to a database table.
          * Each class attribute that is a `models.Field` becomes a database column.
          * Instances of this class represent rows in the table.
        - Conceptually, `Category` is meant to group products (or other entities) into
          named buckets (e.g., "Shoes", "Electronics") and provide a URL-friendly key.
    2) Field: `name`
        - `name = models.CharField(max_length=200)`
        - A `CharField` is a variable-length string column.
        - `max_length=200`:
          * Controls the maximum permitted length at the database/schema level.
          * Is also used by Django forms/validators for input validation.
        - Typical use:                                     
          * Human-readable category label shown in templates/admin.]  mm
    3) Field: `slug`
        - `slug = models.SlugField(max_length=200, unique=True)`
        - `SlugField` is a specialized string field intended for URL-safe identifiers
          (usually lowercased, words separated by hyphens).
        - `max_length=200`:
          * Same role as for `name`, but for the slug.
        - `unique=True`:
          * Adds a uniqueness constraint in the database so no two categories can share
             the same slug.
          * Enables reliable URL patterns like `/category/<slug>/` that map to exactlyffffc5eeddddxxxxxxxxxxxxxxxxxx xxc x x
             one category.
    4) Inner class: `Meta`
        - `class Meta:` configures model-level options that influence how Django
          queries, sorts, and represents the model.
        - `ordering = ['name']`:
          * Sets the default ordering for querysets, so `Category.objects.all()`
             will be returned sorted by `name` ascending unless another ordering is
             specified.
          * This affects admin listing and any implicit ordering.
        - `indexes = [models.Index(fields=['name'])]`:
          * Requests an explicit database index on the `name` column.
          * Improves performance for lookups and sorts that involve `name`, such as:
             - Filtering: `Category.objects.filter(name__icontains='foo')`
             - Ordering (depending on database planner and query shape)
          * The actual SQL index is created when you run migrations.
        - `verbose_name = 'category'`:
          * Human-friendly singular label used in the Django admin and elsewhere.
        - `verbose_name_plural = 'catefories'`:
          * Human-friendly plural label used in the Django admin.
          * Note: the value shown is misspelled; Django will use it as-is.
    5) String representation: `__str__`
        - `def __str__(self) -> str: return self.name`
        - Controls how instances display as text (e.g., in Django admin dropdowns,
          admin list pages, debugging, shell output).
        - Returning `self.name` ensures the category is represented by its readable
          name rather than a generic `Category object (1)`.
    Operational outcome:
    - After migrations, Django creates a damtabase table (typically named
      `shop_category` depending on the app label) with columns for `id` (auto-created
      primary key), `name`, and `slug`.
    - Default queries return categories ordered by name.
    - A database index on `name` and a uniqueness constraint on `slug` are enforced.
    """