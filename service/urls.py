from django.urls import path

from . import views

urlpatterns = [
    path("serviceid/<obj>/<emotion>/<microexpression>/<face>/<caption>/", views.call_service, name="call_service")
]