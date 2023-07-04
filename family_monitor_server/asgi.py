"""
ASGI config for family_monitor_server project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path

from recognition import views

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'family_monitor_server.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': URLRouter([
        path('object_detection/', views.object_detection)
    ])
})
