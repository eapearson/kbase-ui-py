from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("yours", views.yours, name="yours"),
    path("yours/<int:id>", views.yours, name="yours"),
    path("yours/<int:id>/<str:tab>", views.yours, name="yours"),
    path("shared", views.shared, name="shared"),
    path("shared/<int:id>", views.shared, name="shared"),
    path("shared/<int:id>/<str:tab>", views.shared, name="shared"),
    path("tutorial", views.tutorial, name="tutorial"),
    path("tutorial/<int:id>", views.tutorial, name="tutorial"),
    path("tutorial/<int:id>/<str:tab>", views.tutorial, name="tutorial"),
    path("public", views.public, name="public"),
    path("public/<int:id>", views.public, name="public"),
    path("public/<int:id>/<str:tab>", views.public, name="public"),
]
