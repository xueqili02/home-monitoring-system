from django.urls import path

from . import views

urlpatterns = [
    path("object_detection/", views.object_detection, name="object_detection"),
    # path("object_detection/<str:video_name>/", views.object_detection, name="object_detection"),
    # path("<str:video_name>", views.video, name="video")
]