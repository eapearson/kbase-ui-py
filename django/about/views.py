from django.shortcuts import render
from .models import About


# from django.shortcuts import render

# Create your views here.


def index(request):
    about = About.objects.first()
    context = {
        "page": {"title": "About"},
        "about": about,
        "kbase": request.kbase,
    }
    return render(request, "about/index.html", context)


def services(request):
    context = {
        "page": {"title": "KBase Service Status"},
        "kbase": request.kbase,
    }
    return render(request, "about/services.html", context)
