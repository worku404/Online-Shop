"""
Celery configuration for the myshop project.
Sets up the Celery application instance and auto-discovers asynchronous tasks.
"""

import os
from celery import Celery

# 1. Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myshop.settings')

# 2. Create the Celery app instance
app = Celery('myshop')

# 3. Load configuration from Django settings
# Using the 'CELERY' namespace means all celery-related settings 
# must have a 'CELERY_' prefix in settings.py.
app.config_from_object('django.conf:settings', namespace='CELERY')

# 4. Auto-discover tasks from all registered Django apps
app.autodiscover_tasks()