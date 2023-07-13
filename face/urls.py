from django.urls import path

from . import views

urlpatterns = [
    path("upload_image/uid/<uid>/", views.upload_image, name="upload_image"),
    path("face_login/", views.face_login, name="face_login"),
    path("intrusion_recognition/uid/<uid>/", views.intrusion_recognition, name="intrusion_recognition"),
    path("intrusion_record/uid/<uid>/", views.intrusion_record, name="intrusion_record"),
    path("intrusion_video/", views.intrusion_video, name="intrusion_video"),
]