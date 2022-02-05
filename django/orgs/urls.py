from django.urls import path
from . import views

urlpatterns = [
    path("own", views.own, name="own"),
    path("own/<str:id>", views.own, name="own"),
    path("member", views.member, name="member"),
    path("member/<str:id>", views.member, name="member"),
    path("public", views.public, name="public"),
    path("public/<str:id>", views.public, name="public"),
    path("", views.index, name="index"),
    path("<str:id>", views.index, name="index"),
]
