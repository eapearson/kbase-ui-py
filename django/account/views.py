from django.shortcuts import render


def index(request):
    return render(
        request,
        "account/index.html",
        {"page": {"title": "Account"}, "kbase": request.kbase},
    )
