# chat/routing.py
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/video/(?P<video_name>\w+)/$", consumers.ObjectDetectionConsumer.as_asgi()),
]