from django.urls import path

from . import views

urlpatterns = [
    path("emotion_recognition/", views.emotion_recognition, name="emotion_recognition"),
]