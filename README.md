# My Shop (Django E-commerce)

My Shop is a multilingual, full-stack e-commerce web application built with Django.  
It includes a complete customer purchase flow: catalog browsing, cart management, coupon discounts, weighted shipping, Stripe checkout, webhook-based payment confirmation, invoice generation, and Redis-powered product recommendations.

## Highlights
- End-to-end checkout and payment workflow
- Stripe Checkout integration + secure webhook verification
- Dynamic shipping cost based on product weight
- Coupon system with time-window validation
- Session-based cart with quantity updates and stale-item cleanup
- Product recommendations using Redis co-purchase scoring
- Multilingual UI and translated URLs (`en`, `es`, `am`)
- Async task processing with Celery (emails + PDF invoices)
- Admin tooling for orders, CSV export, and invoice access

## Tech Stack
- Python 3
- Django 6
- SQLite (default)
- Stripe API
- Redis
- Celery
- WeasyPrint
- django-parler
- django-rosetta
- django-localflavor

## Core Features

### Customer Features
- Product listing and category filtering
- Product details with quantity selection
- Cart add/update/remove
- Coupon apply
- Checkout form with Ethiopian postal code validation
- Shipping + total calculation
- Stripe payment page and payment status pages
- "People who bought this also bought" recommendations

### Business/Admin Features
- Product/category management (with translations)
- Coupon management
- Order management with inline order items
- Stripe payment ID visibility in admin
- Order CSV export
- PDF invoice generation and email delivery

## Quick Start

From repository root:

```powershell
cd myshop
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

In separate terminals:

```powershell
# Redis
redis-server
```

```powershell
# Celery worker
cd myshop
celery -A myshop worker -l info
```

```powershell
# Stripe webhook forwarding
stripe listen --forward-to http://127.0.0.1:8000/payment/webhook/
```

## Environment Variables
Create `myshop/.env`:

```env
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

## Project Layout
```text
onlineShop/
  README.md
  myshop/
    manage.py
    requirements.txt
    myshop/           # settings, urls, celery
    shop/             # catalog, recommender
    cart/             # session cart
    coupons/          # coupon rules
    orders/           # checkout, models, PDF/admin
    payment/          # stripe process/webhooks/tasks
    locale/           # en/es/am translations
```

## Architecture Snapshot
1. User adds products to session cart.
2. User applies coupon (optional).
3. Checkout creates order + order items, computes shipping.
4. Payment page creates Stripe Checkout session from stored order items.
5. Stripe webhook marks order as paid.
6. Celery task sends invoice email with attached PDF.
7. Redis recommendation scores are updated from paid order items.

## Documentation
- Full technical documentation: [`myshop/README.md`](myshop/README.md)

## Current Status
This project is complete and functional for local development and portfolio demonstration.  
Before production deployment, harden security/configuration (`DEBUG`, `ALLOWED_HOSTS`, secret management, database, static/media strategy, monitoring).


