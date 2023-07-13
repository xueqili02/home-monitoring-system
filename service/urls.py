from django.urls import path

from . import views

urlpatterns = [
    path("serviceid/<obj>/<emotion>/<microexpression>/<face>/", views.call_service, name="call_service"),
    path("image_caption/", views.image_caption, name="image_caption"),
    path("three_to_two/", views.three_to_two, name="three_to_two"),
]