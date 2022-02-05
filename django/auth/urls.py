from django.urls import path

from . import views

urlpatterns = [
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("loginstart", views.loginstart, name="loginstart"),
    path("logincontinue", views.logincontinue, name="logincontinue"),
    path("", views.index, name="index"),
]
