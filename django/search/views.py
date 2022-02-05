from django.shortcuts import render


def index(request):
    return render(
        request,
        "search/index.html",
        {"page": {"title": "Search"}, "kbase": request.kbase},
    )
