from django.urls import path

from . import views

urlpatterns = [
    path("load", views.load, name="load"),
    path("", views.index, name="index"),
]
