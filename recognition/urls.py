from django.urls import path

from . import views

urlpatterns = [
    path("object_detection/", views.object_detection, name="object_detection"),
]