from django.urls import path

from . import views

urlpatterns = [
    path("upload_image/<uid>/", views.upload_image, name="upload_image"),
    path("face_login/", views.face_login, name="face_login"),
]