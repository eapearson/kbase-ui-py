# import json
from dateutil.parser import parse
from django.conf import settings
from django.shortcuts import render, redirect

from lib.GenericClient2 import GenericClient2
from lib.RESTClient import RESTClient
from lib.utils import utc_from_epoch_ms, utc_from_string

SEARCHAPI_URL = settings.KBASE["services"]["search"]["url"]
AUTH_URL = settings.KBASE["services"]["auth"]["url"]


def get_narratives(filter, auth_token, owner):
    client = GenericClient2(
        url=SEARCHAPI_URL, module=None, token=auth_token, timeout=60
    )
    query = {"bool": {"must": [], "must_not": [{"term": {"is_temporary": True}}]}}
    if filter == "own":
        query["bool"]["must"].append({"term": {"owner": owner}})
    elif filter == "shared":
        query["bool"]["must"].append({"term": {"shared_users": owner}})
        query["bool"]["must_not"].append({"term": {"owner": owner}})
    try:
        result = client.call_func(
            "search_objects",
            {
                "query": query,
                "from": 0,
                "size": 1000,
                "indexes": ["narrative"],
                "sort": [{"timestamp": {"order": "desc"}}, "_score"],
                "track_total_hits": True,
            },
        )
        error = None
    except Exception as e:
        return None, {"exception": e, "message": str(e)}

    # Okay, format the data into something friendlier; also, we can
    # handle transforming in Python rather than in the template.

    narratives = []
    for hit in result["hits"]:
        created_at = utc_from_string(hit["doc"]["creation_date"])
        modified_at = utc_from_epoch_ms(hit["doc"]["modified_at"])

        narratives.append(
            {
                "id": hit["doc"]["access_group"],
                "title": hit["doc"]["narrative_title"],
                "owner": hit["doc"]["owner"],
                "created_at": created_at,
                "modified_at": modified_at,
                "cell_count": len(hit["doc"]["cells"]),
                "object_count": len(hit["doc"]["data_objects"]),
            }
        )

    return {"total_count": result["count"], "narratives": narratives}, None


# Create your views here.
def error(request):
    return render(
        request,
        "dashboard/error.html",
        {
            "page": {"title": "Dashboard - ERROR"},
            "kbase": request.kbase,
        },
    )


def index(request):
    # Build up the narratives and other stuff...

    if "error" in request.kbase:
        return render(
            request,
            "error",
            {
                "page": {"title": "Dashboard"},
                "error": request.kbase["error"],
                "kbase": request.kbase,
            },
        )

    if not request.kbase["is_authenticated"]:
        # return render(request, 'error/index.html')
        # print(
        #     "NOT AUTH",
        #     request.path,
        #     request.COOKIES,
        #     request.META,
        #     request.headers,
        # )
        return redirect(f"/auth/login?path={request.path}")

    auth_token = request.COOKIES["kbase_session"]

    authService = RESTClient(url=AUTH_URL, timeout=60, token=auth_token)

    me = authService.get("api/V2/me")
    username = me["user"]
    # realname = me['display']

    own_narratives, error = get_narratives("own", auth_token, username)
    shared_narratives, error = get_narratives("shared", auth_token, username)

    return render(
        request,
        "dashboard/index.html",
        {
            "page": {"title": "Dashboard"},
            "your_narratives": own_narratives,
            "shared_narratives": shared_narratives,
            "error": error,
            "kbase": request.kbase,
        },
    )
