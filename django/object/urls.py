from django.urls import path
from . import views

urlpatterns = [
    path("<str:workspace>/<str:object>", views.index, name="index"),
    path("<str:workspace>/<str:object>/<int:object_version>", views.index, name="index"),
    path("<str:workspace>/<str:object>/overview", views.overview, name="overview"),
    path("<str:workspace>/<str:object>/<int:object_version>/overview", views.overview, name="overview"),
    path("<str:workspace>/<str:object>/provenance", views.provenance, name="provenance"),
    path("<str:workspace>/<str:object>/<int:object_version>/provenance", views.provenance, name="provenance"),
    path("<str:workspace>/<str:object>/related-data", views.related_data, name="related_data"),
    path("<str:workspace>/<str:object>/<int:object_version>/related-data", views.related_data, name="related_data"),
    path("<str:workspace>/<str:object>/linkted-samples", views.linked_samples, name="linked_samples"),
    path("<str:workspace>/<str:object>/<int:object_version>/linked-samples", views.linked_samples, name="linked_samples"),
]
