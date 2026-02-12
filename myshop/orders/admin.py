"""
Admin configuration for the orders application.
Includes custom actions for CSV export and custom columns for 
Stripe payments, PDF invoices, and detailed views.
"""

import csv
import datetime
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.http import HttpResponse
from django.urls import reverse

from .models import Order, OrderItem

# ==============================================================================
# ACTIONS
# ==============================================================================

def export_to_csv(modeladmin, request, queryset):
    """
    Generic admin action to export selected models to a CSV file.
    Excludes Many-to-Many and One-to-Many fields to keep it flat.
    """
    opts = modeladmin.model._meta
    content_disposition = f'attachment; filename={opts.verbose_name}.csv'
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = content_disposition
    writer = csv.writer(response)
    
    # Get physical fields of the model
    fields = [
        field for field in opts.get_fields() 
        if not field.many_to_many and not field.one_to_many
    ]
    
    # Write header row
    writer.writerow([field.verbose_name for field in fields])
    
    # Write data rows
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    
    return response

export_to_csv.short_description = 'Export to CSV'


# ==============================================================================
# COLUMN HELPERS (Custom Display Fields)
# ==============================================================================

def order_payment(obj):
    """Displays a clickable link to the Stripe dashboard for this order."""
    url = obj.get_stripe_url()
    if obj.stripe_id:
        html = f'<a href="{url}" target="_blank">{obj.stripe_id}</a>'
        return mark_safe(html)
    return ''

order_payment.short_description = 'Stripe Payment'


def order_detail(obj):
    """Displays a link to the custom admin detail view."""
    url = reverse('orders:admin_order_detail', args=[obj.id])
    return mark_safe(f'<a href="{url}">View</a>')


def order_pdf(obj):
    """Displays a link to download the PDF invoice."""
    url = reverse('orders:admin_order_pdf', args=[obj.id])
    return mark_safe(f'<a href="{url}">PDF</a>')

order_pdf.short_description = 'Invoice'


# ==============================================================================
# INLINES
# ==============================================================================

class OrderItemInline(admin.TabularInline):
    """Allows managing Order Items directly within the Order admin page."""
    model = OrderItem
    raw_id_fields = ['product']


# ==============================================================================
# MODEL REGISTRATION
# ==============================================================================

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for the Order model.
    Includes custom filters, search, inlines, and CSV export action.
    """
    list_display = [
        'id', 'first_name', 'last_name', 'email', 
        'address', 'postal_code', 'city', 'paid',
        order_payment, 'created', 'updated', 
        order_detail, order_pdf
    ]
    list_filter = ['paid', 'created', 'updated']
    search_fields = ['first_name', 'last_name', 'email']
    inlines = [OrderItemInline]
    actions = [export_to_csv]