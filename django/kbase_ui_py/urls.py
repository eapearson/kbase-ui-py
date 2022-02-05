"""kbase_ui_py URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("about/", include("about.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("navigator/", include("navigator.urls")),
    path("user_profile/<str:username>", include("user_profile.urls")),
    path("catalog/", include("catalog.urls")),
    path("feeds/", include("feeds.urls")),
    path("auth/", include("auth.urls")),
    path("load-narrative.html", include("narrative_manager.urls")),
    path("narrative_manager/", include("narrative_manager.urls")),
    path("orgs/", include("orgs.urls")),
    path("search/", include("search.urls")),
    path("jobs/", include("jobs.urls")),
    path("account/", include("account.urls")),
    path("object/", include("object.urls")),
    path("type/", include("type.urls")),
    path("biochem-search/", include("biochem_search.urls")),
    path("samples/", include("samples.urls")),
    path("", include("dashboard.urls")),
]
