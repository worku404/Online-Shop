"""
Django settings module for the myshop project.
Grouped into logical sections for better maintainability.
"""

from pathlib import Path
from decouple import config

# ==============================================================================
# CORE SETTINGS
# ==============================================================================

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-p8!t4&yh^xu+i7vswg*o#_$(9tj8e-b+_gn0-y$k4!nisa%6kv'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

ROOT_URLCONF = 'myshop.urls'
WSGI_APPLICATION = 'myshop.wsgi.application'


# ==============================================================================
# APPS & MIDDLEWARE
# ==============================================================================

INSTALLED_APPS = [
    # Django Default Apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Custom Apps
    'cart.apps.CartConfig',
    'shop.apps.ShopConfig',
    'orders.apps.OrdersConfig',
    'payment.apps.PaymentConfig',
    'coupons.apps.CouponsConfig',
    'rosetta',
    'parler',
    'localflavor',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'cart.context_processors.cart',
            ],
        },
    },
]


# ==============================================================================
# DATABASE
# ==============================================================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# ==============================================================================
# AUTHENTICATION & PASSWORD VALIDATION
# ==============================================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# ==============================================================================
# INTERNATIONALIZATION
# ==============================================================================
from django.conf.locale import LANG_INFO
from django.utils.translation import gettext_lazy as _

LANG_INFO.update({
    'am': {
        'bidi': False,
        'code': 'am',
        'name': 'Amharic',
        'name_local': 'አማርኛ',
    },
})

LANGUAGE_CODE = 'en'
LANGUAGES = [
    ('en', _('English')),
    ('es', _('Spanish')),       # Common second language
    ('am', _('Amharic')),
]
LOCALE_PATHS = [
    BASE_DIR / 'locale',
]
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

PARLER_LANGUAGES = {
    None: (
        {'code': 'en'},
        {'code': 'es'},
        {'code': 'am'},
        
    ),
    'default': {
        'fallbacks': ['en'],
        'hide_untranslated': False,
    }
}
# ==============================================================================
# STATIC & MEDIA FILES
# ==============================================================================

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'


# ==============================================================================
# THIRD-PARTY APIS & INTEGRATIONS
# ==============================================================================

# Stripe Configuration
STRIPE_PUBLISHABLE_KEY = config('STRIPE_PUBLISHABLE_KEY')
STRIPE_SECRET_KEY = config('STRIPE_SECRET_KEY')
STRIPE_WEBHOOK_SECRET = config('STRIPE_WEBHOOK_SECRET')
# STRIPE_API_VERSION= '2026-01-28'

# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# ==============================================================================
# CUSTOM PROJECT SETTINGS
# ==============================================================================

CART_SESSION_ID = 'cart'


# ========================================
# Redis settings
# =======================================
REDIS_HOST = 'localhost'
REDIS_PORT = '6379'
REDIS_DB = 1