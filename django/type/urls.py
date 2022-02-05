from django.urls import path
from . import views

urlpatterns = [
    path("module/<str:module>/<str:version>", views.module, name="module"),
    path("module/<str:module>/<str:version>/<str:tab>", views.module, name="module"),
    path("<str:type>", views.index, name="index"),
    path("<str:type>/<str:tab>", views.index, name="index"),
    path("module/<str:module>", views.module, name="module"),
]
