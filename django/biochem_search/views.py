from django.shortcuts import render


def index(request):
    return render(
        request,
        "biochem_search/index.html",
        {"page": {"title": "Biochem Search"}, "kbase": request.kbase},
    )
