from django.shortcuts import render
from django.conf import settings
from lib.GenericClient import GenericClient

nms_url = settings.KBASE["services"]["narrative_method_store"]["url"]
catalog_url = settings.KBASE["services"]["catalog"]["url"]


def index(request):

    # token_cookie_name = settings.KBASE["config"]["token_cookie_name"]

    # if token_cookie_name not in request.COOKIES:
    #     return render(request, "error/index.html")

    auth_token = request.COOKIES.get("kbase_session")

    catalog_service = GenericClient(
        module="NarrativeMethodStore",
        url=nms_url,
        timeout=60,
        token=auth_token,
    )

    apps = catalog_service.call_func(
        "list_methods",
        {"tag": None},
    )

    return render(
        request,
        "catalog/index.html",
        {
            "page": {"title": "Catalog - Home"},
            "apps": apps,
            "kbase": request.kbase,
        },
    )


def apps(request):

    # token_cookie_name = settings.KBASE["config"]["token_cookie_name"]

    # if token_cookie_name not in request.COOKIES:
    #     return render(request, "error/index.html")

    auth_token = request.COOKIES.get("kbase_session")

    catalog_service = GenericClient(
        module="NarrativeMethodStore",
        url=nms_url,
        timeout=60,
        token=auth_token,
    )

    apps = catalog_service.call_func(
        "list_methods",
        {"tag": None},
    )

    return render(
        request,
        "catalog/apps.html",
        {
            "page": {"title": "Catalog - Apps"},
            "apps": apps,
            "kbase": request.kbase,
        },
    )


def modules(request):

    # token_cookie_name = settings.KBASE["config"]["token_cookie_name"]

    # if token_cookie_name not in request.COOKIES:
    #     return render(request, "error/index.html")

    auth_token = request.COOKIES.get("kbase_session")

    catalog_service = GenericClient(
        module="Catalog",
        url=catalog_url,
        timeout=60,
        token=auth_token,
    )

    modules = catalog_service.call_func(
        "list_basic_module_info",
        {
            "include_released": 1,
            "include_unreleased": 1,
            "include_disabled": 1,
            "include_modules_with_no_name_set": 1,
        },
    )

    return render(
        request,
        "catalog/modules.html",
        {
            "page": {"title": "Catalog - Modules"},
            "modules": modules,
            "kbase": request.kbase,
        },
    )
