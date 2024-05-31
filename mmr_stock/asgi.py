"""
ASGI config for mmr_stock project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from dash.urls import ws_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mmr_stock.settings')

application = ProtocolTypeRouter(
  {
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(URLRouter(ws_urlpatterns))
  }
)
