from django.urls import path

from . import views

urlpatterns = [
    path("object_recognition/", views.object_recognition, name="object_recognition"),
    path("camera/<uid>/", views.camera, name="camera"),
    path("range_coordinate/", views.range_coordinate, name="range_coordinate"),
    path("first_image/", views.first_image, name="first_image"),
    path("active_objects/", views.active_objects, name="active_objects"),
    path("record/<uid>/", views.record, name="record"),
    path("object_image/", views.object_image, name="object_image"),
]