"""
The URL configuration module integrates Django’s URL dispatcher with the rest of the project. The line `path('', include('shop.urls', namespace='shop'))` tells Django to delegate any request not captured by `admin/` to the URL definitions inside the `shop` application, creating a namespace so reverse lookups remain unambiguous. This delegation works because `settings.py` references `INSTALLED_APPS` to activate `shop`, and when Django loads the project it imports this `urls.py`, so the root URL resolver now pulls in `shop.urls`.
The conditional block `if settings.DEBUG: urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)` hooks into the project’s settings by reading `settings.MEDIA_URL` and `settings.MEDIA_ROOT` defined in `settings.py`; this configuration instructs Django to serve media files directly during development, effectively extending `urlpatterns` to include URL patterns pointing to the media folder.
Example data flow:
1. A user hits `/` in their browser.
2. Django starts matching URLs against `urlpatterns` in this file.ĪĒ
3. Because the path is `''`, Django calls into `shop.urls`, resolving to one of the view functions defined there.
4. If the view needs uploaded media like `/media/images/example.jpg`, Django uses the static-serving patterns added when `settings.DEBUG` is `True`, which reference the `MEDIA_ROOT` folder from `settings.py` and streams the file back to the browser.
URL configuration for myshop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import viewsĒĒ
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cart/', include('cart.urls', namespace='cart')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('', include('shop.urls', namespace='shop')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )