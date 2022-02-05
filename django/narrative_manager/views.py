from django.shortcuts import render


def load(request):
    return render(
        request,
        "narrative_manager/load.html",
        {
            "page": {"title": "Narrative Manager - Loader"},
            "kbase": request.kbase,
        },
    )


def index(request):
    if request.path == "/load-narrative.html":
        return render(
            request,
            "narrative_manager/load.html",
            {
                "page": {"title": "Narrative Manager - Loader"},
                "kbase": request.kbase,
            },
        )
    else:
        return render(
            request,
            "narrative_manager/index.html",
            {
                "page": {"title": "Narrative Manager"},
                "kbase": request.kbase,
            },
        )
