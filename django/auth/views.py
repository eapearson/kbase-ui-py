from lib.RESTClient import RESTClient, RESTError
from django.shortcuts import render, redirect
from django.conf import settings

# Create your views here.

from django.shortcuts import render


def index(request):
    return render(request, "auth/index.html")


def loginstart(request):
    return render(request, "auth/loginstart.html", {"status": "OK"})


def logincontinue(request):
    return render(request, "auth/logincontinue.html", {"status": "OK"})


def login(request):
    if request.kbase["is_authenticated"]:
        return render(
            request,
            "about.html",
            {
                "page": {"title": "Dashboard"},
                "kbase": request.kbase,
                "settings": settings.KBASE,
            },
        )

    # auth_token = request.kbase["auth"]["token"]
    # auth_url = settings.KBASE["services"]["auth"]["url"]
    # auth_service = RESTClient(url=auth_url, timeout=60, token=auth_token)
    # login_choice, err = auth_service.get(
    #     "login/choice", extra_header={"Cookie": f"kbase_session={auth_token}"}
    # )

    login_start_url = settings.KBASE["services"]["auth"]["url"]

    return render(
        request,
        "auth/login.html",
        {
            "login_start_url": f"{login_start_url}/login/start",
            "path": request.path,
            "settings": settings.KBASE,
        },
    )


def logout(request):
    # response = HttpResponse()
    auth_token = request.kbase["auth"]["token"]
    if auth_token is not None:

        auth_url = settings.KBASE["services"]["auth"]["url"]
        auth_service = RESTClient(url=auth_url, timeout=60, token=auth_token)
        try:
            auth_service.post(
                "logout", extra_header={"Cookie": f"kbase_session={auth_token}"}
            )
        except RESTError as re:
            print("auth error", re.code, re.data)

        response = redirect("/auth/login")
        response.delete_cookie("kbase_session")
        return response

    return redirect("/auth/login")
