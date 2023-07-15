from django.urls import path

from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("information/uid/<uid>/", views.information, name="information"),
    path("allinformation/", views.allinformation, name="information"),
]
