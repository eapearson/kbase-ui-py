from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("apps", views.apps, name="apps"),
    path("modules", views.modules, name="modules"),
]
