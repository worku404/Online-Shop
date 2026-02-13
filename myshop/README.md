# My Shop

A multilingual Django e-commerce application with product catalog management, cart and coupon handling, weighted shipping, Stripe checkout, Redis-powered product recommendations, and asynchronous order/payment tasks.

## Table of Contents
- Project Overview
- Key Features
- Technology Stack
- Architecture and Workflow
- Project Structure
- Prerequisites
- Installation
- Configuration
- Running the Project
- Usage Guide
- Internationalization
- Admin Features
- Important Routes
- Recommendation Engine Notes
- Testing
- Production Readiness Checklist

## Project Overview
My Shop is a full-stack Django web application designed to support a complete online purchasing flow:

1. Browse products and categories
2. Add items to cart and update quantities
3. Apply coupon discounts
4. Create an order with shipping and postal validation
5. Pay through Stripe Checkout
6. Confirm payment via Stripe webhooks
7. Trigger post-payment tasks and recommendation updates

The application includes multilingual support for English (`en`), Spanish (`es`), and Amharic (`am`), with translated URL segments and translated product/category content.

## Key Features

### Storefront and Catalog
- Category and product catalog pages
- Product detail pages with image, description, and quantity selector
- Product and category translations powered by `django-parler`
- Availability flag and timestamp tracking on products
- Product weight field (grams) for shipping computation

### Cart and Coupons
- Session-based cart persistence
- Quantity updates and item removal
- Automatic cleanup of stale cart rows when referenced products no longer exist
- Coupon application with date-window and active-state validation
- Cart totals:
  - Subtotal
  - Coupon discount
  - Shipping
  - Final total

### Checkout and Orders
- Checkout form with Ethiopian postal code validation (`exactly 4 digits`)
- Order model with line items, discount, shipping cost, and total weight
- Shipping cost tiers based on total weight:
  - `0g`: free shipping (`0.00`)
  - `<= 1000g`: `5.00`
  - `<= 5000g`: `10.00`
  - `> 5000g`: `20.00`
- Checkout guards to prevent creating/paying empty orders

### Payments and Webhooks
- Stripe Checkout session creation with order line items
- Optional shipping line item (only when chargeable)
- Coupon discounts passed to Stripe via generated Stripe coupon
- Success and cancellation pages
- Webhook endpoint (`/payment/webhook/`) to:
  - validate Stripe signature
  - mark order as paid
  - store Stripe payment intent ID
  - update recommendation data
  - trigger post-payment async task

### Recommendations
- Redis sorted-set based "products bought together" recommender
- Recommendations shown on:
  - Product detail page
  - Cart page
- Recommendations improve after successful paid multi-item orders

### Asynchronous Tasks
- `orders.tasks.order_created`: sends order confirmation email
- `payment.tasks.payment_completed`: generates PDF invoice and emails it
- Celery auto-discovery enabled

### Admin and Backoffice
- Category/Product management with translated fields
- Coupon management
- Order admin with:
  - inline order items
  - Stripe payment link
  - PDF invoice link
  - CSV export action
  - custom detail view

### Internationalization
- UI translation with Django i18n
- Language switcher in header
- Translated route prefixes via `i18n_patterns`
- Rosetta integration for translation editing

## Technology Stack
- Python 3
- Django
- SQLite (default)
- Stripe API
- Redis
- Celery
- WeasyPrint
- django-parler
- django-rosetta
- django-localflavor
- python-decouple

## Architecture and Workflow

1. User adds products to session cart.
2. User optionally applies a coupon.
3. User submits checkout form.
4. System creates order and order items, computes shipping, clears cart, stores `order_id` in session.
5. User is redirected to payment process page.
6. Stripe Checkout session is created from persisted order items.
7. Stripe webhook confirms payment.
8. System marks order paid, updates recommendations in Redis, and sends invoice email asynchronously.

## Project Structure
```text
myshop/
  manage.py
  myshop/
    settings.py
    urls.py
    celery.py
  shop/
    models.py
    views.py
    recommender.py
    templates/shop/
    static/shop/css/
  cart/
    cart.py
    views.py
    templates/cart/
  coupons/
    models.py
    forms.py
    views.py
  orders/
    models.py
    forms.py
    validators.py
    views.py
    tasks.py
    templates/orders/
    templates/admin/orders/
  payment/
    views.py
    webhooks.py
    tasks.py
    templates/payment/
  locale/
    en/
    es/
    am/
```

## Prerequisites
- Python 3.10+ (project currently used with Python 3.13)
- Redis server running locally
- Stripe account and API keys
- Stripe CLI (for local webhook forwarding)
- GNU gettext (for `makemessages` and `compilemessages`)
- OS dependencies required by WeasyPrint

## Installation

From the repository root:

```powershell
cd myshop
python -m venv .venv
.venv\Scripts\activate
pip install Django celery redis stripe python-decouple WeasyPrint Pillow django-parler django-rosetta django-localflavor
```

Apply migrations:

```powershell
python manage.py migrate
```

Create an admin user:

```powershell
python manage.py createsuperuser
```

## Configuration

Create a `.env` file in the same directory as `manage.py` (`myshop/`) with:

```env
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

Important notes:
- `SECRET_KEY` is currently hardcoded in `settings.py`. Move it to environment variables for production.
- `DEBUG=True` and `ALLOWED_HOSTS=[]` are development defaults.
- Email backend is currently console backend (`django.core.mail.backends.console.EmailBackend`).

## Running the Project

Start Django:

```powershell
python manage.py runserver
```

Start Redis:

```powershell
redis-server
```

Start Celery worker (if async tasks are enabled in your environment):

```powershell
celery -A myshop worker -l info
```

Forward Stripe webhooks to local app:

```powershell
stripe listen --forward-to http://127.0.0.1:8000/payment/webhook/
```

Then copy the webhook secret from Stripe CLI output into `.env` as `STRIPE_WEBHOOK_SECRET`.

## Usage Guide

### 1. Prepare Catalog Data
- Log in to `/admin/`
- Create categories and products
- Add translations for each category/product as needed
- Set `weight` for products to enable shipping calculations

### 2. Shop as User
- Visit localized storefront (`/en/`, `/es/`, `/am/`)
- Add products to cart
- Apply a coupon (optional)
- Proceed to checkout

### 3. Checkout
- Fill customer details and Ethiopian postal code
- Review shipping and total
- Place order

### 4. Payment
- Open payment summary page
- Click `Pay now` to go to Stripe Checkout
- Complete payment

### 5. Post-Payment
- Stripe webhook marks order as paid
- PDF invoice email task runs
- Recommendation co-purchase data updates in Redis

## Internationalization

Languages configured:
- English (`en`)
- Spanish (`es`)
- Amharic (`am`)

Translation workflow:

```powershell
python manage.py makemessages -l es -l am
python manage.py compilemessages
```

Rosetta is available at:
- `/rosetta/`

## Admin Features
- Product and category management with translated fields
- Coupon creation and activation windows
- Order list with:
  - payment status
  - Stripe payment link
  - CSV export
  - PDF invoice generation
  - custom order detail page

## Important Routes

Localized routes are prefixed by language code (for example `/en/...`, `/es/...`, `/am/...`):

- Storefront: `/`
- Cart: `/cart/`
- Orders: `/orders/create/`
- Payment process: `/payment/process/`
- Payment completed: `/payment/completed/`
- Payment canceled: `/payment/canceled/`
- Coupons apply: `/coupons/apply/`

Non-localized webhook route:
- Stripe webhook: `/payment/webhook/`

## Recommendation Engine Notes
- Recommendations are based on products bought together in paid orders.
- If recommendations are empty, verify:
  - Redis is running
  - Webhook delivery is successful
  - Orders were completed and marked as paid
  - Orders contain more than one product to build co-purchase links

## Testing
- Test modules exist per app but are currently placeholders.
- Run checks:

```powershell
python manage.py check
```

## Production Readiness Checklist
- Move `SECRET_KEY` to environment variable
- Set `DEBUG=False`
- Configure `ALLOWED_HOSTS`
- Use a production DB (for example PostgreSQL)
- Configure static/media serving strategy
- Configure secure email backend
- Configure Celery broker/result backend explicitly
- Add automated tests for checkout, payment webhook, and recommendation logic
- Add monitoring/logging for webhook and task execution

