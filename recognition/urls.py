from django.urls import path

from . import views

urlpatterns = [
    path("object_recognition/", views.object_recognition, name="object_recognition"),
    path("camera/uid/<uid>/cid/<cid>/", views.camera, name="camera"),
    path("range_coordinate/", views.range_coordinate, name="range_coordinate"),
    path("first_image/", views.first_image, name="first_image"),
    path("active_objects/", views.active_objects, name="active_objects"),
    path("record/uid/<uid>/", views.record, name="record"),
    path("object_image/", views.object_image, name="object_image"),
    path("camera_url/", views.camera_url, name="camera_url"),
]