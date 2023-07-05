from django.urls import path

from . import views

urlpatterns = [
    path("expression_recognition/", views.expression_recognition, name="expression_recognition"),
]