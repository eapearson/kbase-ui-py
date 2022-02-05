from django.shortcuts import render, redirect
from . import kbmodel


# Create your views here.
def index(request):
    if not request.kbase["is_authenticated"]:
        return redirect(f"/auth/login?path={request.path}")

    totals = kbmodel.get_narrative_totals(
        request.kbase["auth"]["token"], request.kbase["auth"]["me"]["user"]
    )
    return render(
        request,
        "navigator/index.html",
        {
            "page": {"title": "Narratives Navigator"},
            "kbase": request.kbase,
            "request": {"path": request.path.rstrip("/")},
            "totals": totals,
        },
    )


def shared(request, id=None, tab=None):
    if not request.kbase["is_authenticated"]:
        return redirect(f"/auth/login?path={request.path}")

    narratives = kbmodel.get_narratives(
        "shared", request.kbase["auth"]["token"], request.kbase["auth"]["me"]["user"]
    )
    totals = kbmodel.get_narrative_totals(
        request.kbase["auth"]["token"], request.kbase["auth"]["me"]["user"]
    )

    if id is None and len(narratives) > 0:
        id = narratives["narratives"][0]["id"]

    if tab is None:
        tab = "data"

    narrative = None
    if id:
        narrative = kbmodel.get_narrative(
            id, request.kbase["auth"]["token"], request.kbase["auth"]["me"]["user"]
        )
    return render(
        request,
        "navigator/navigator.html",
        {
            "page": {
                "title": "Narratives Navigator - Shared With Me",
                "tab1": "shared",
                "tab2": tab,
            },
            "kbase": request.kbase,
            "narratives": narratives,
            "selected_narrative": narrative,
            "request": {"path": request.path.rstrip("/")},
            "totals": totals,
        },
    )


def tutorial(request, id=None, tab=None):
    if not request.kbase["is_authenticated"]:
        return redirect(f"/auth/login?path={request.path}")

    narratives = kbmodel.get_narratives(
        "tutorial", request.kbase["auth"]["token"], request.kbase["auth"]["me"]["user"]
    )
    totals = kbmodel.get_narrative_totals(
        request.kbase["auth"]["token"], request.kbase["auth"]["me"]["user"]
    )

    if id is None and len(narratives) > 0:
        id = narratives["narratives"][0]["id"]

    if tab is None:
        tab = "data"

    narrative = None
    if id:
        narrative = kbmodel.get_narrative(
            id, request.kbase["auth"]["token"], request.kbase["auth"]["me"]["user"]
        )
    return render(
        request,
        "navigator/navigator.html",
        {
            "page": {
                "title": "Narratives Navigator - Tutorial Narratives",
                "tab1": "tutorial",
                "tab2": tab,
            },
            "kbase": request.kbase,
            "narratives": narratives,
            "selected_narrative": narrative,
            "request": {"path": request.path.rstrip("/")},
            "totals": totals,
        },
    )


def public(request, id=None, tab=None):
    if not request.kbase["is_authenticated"]:
        return redirect(f"/auth/login?path={request.path}")

    narratives = kbmodel.get_narratives(
        "public", request.kbase["auth"]["token"], request.kbase["auth"]["me"]["user"]
    )
    totals = kbmodel.get_narrative_totals(
        request.kbase["auth"]["token"], request.kbase["auth"]["me"]["user"]
    )

    if id is None and len(narratives) > 0:
        id = narratives["narratives"][0]["id"]

    if tab is None:
        tab = "data"

    narrative = None
    if id:
        narrative = kbmodel.get_narrative(
            id, request.kbase["auth"]["token"], request.kbase["auth"]["me"]["user"]
        )
    return render(
        request,
        "navigator/navigator.html",
        {
            "page": {
                "title": "Narratives Navigator - Public Narratives",
                "tab1": "public",
                "tab2": tab,
            },
            "kbase": request.kbase,
            "narratives": narratives,
            "selected_narrative": narrative,
            "request": {"path": request.path.rstrip("/")},
            "totals": totals,
        },
    )


def yours(request, id=None, tab=None):
    if not request.kbase["is_authenticated"]:
        return redirect(f"/auth/login?path={request.path}")

    try: 
        narratives = kbmodel.get_narratives(
            "own", request.kbase["auth"]["token"], request.kbase["auth"]["me"]["user"]
        )
        # print(narratives["narratives"][0])
        totals = kbmodel.get_narrative_totals(
            request.kbase["auth"]["token"], request.kbase["auth"]["me"]["user"]
        )

        if id is None and len(narratives) > 0:
            id = narratives["narratives"][0]["id"]

        if tab is None:
            tab = "data"

        narrative = None
        if id:
            narrative = kbmodel.get_narrative(
                id, request.kbase["auth"]["token"], request.kbase["auth"]["me"]["user"]
            )
        return render(
            request,
            "navigator/navigator.html",
            {
                "page": {"title": "Narratives Navigator", "tab1": "yours", "tab2": tab},
                "kbase": request.kbase,
                "narratives": narratives,
                "selected_narrative": narrative,
                "request": {"path": request.path.rstrip("/")},
                "totals": totals,
            },
        )
    except Exception as ex:
        print('error')
        print(str(ex))
        return render(request, "error/index.html", {
                "page": {"title": "Error"},
                "error": str(ex),
                "kbase": request.kbase,
                "request": request
            })
