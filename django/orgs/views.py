from django.shortcuts import render
from django.conf import settings
from lib.RESTClient import RESTClient, RESTError
import datetime

base_url = settings.KBASE["service_base_url"]


def get_groups(
    request, query=None, only_owner=False, only_member=False, only_public=False
):
    auth_token = request.kbase["auth"]["token"]
    groups_service = RESTClient(
        url=f"{base_url}/services/groups",
        token=auth_token,
        timeout=60,
    )

    groups = groups_service.get("group")

    # Get all orgs this user can see
    filtered_groups = []
    total_own = 0
    total_member = 0
    total_public = 0
    total_filtered_own = 0
    total_filtered_member = 0
    total_filtered_public = 0
    current_username = request.kbase["auth"]["me"]["user"]
    if query is not None:
        query_lower = query.lower()
    else:
        query_lower = None
    for group in groups:
        keep = True

        # Search query
        if query_lower is not None:
            if query_lower in group["owner"] or query_lower in group["name"].lower():
                keep = True
            else:
                keep = False

        # Calc totals for different types
        if group["role"] == "Owner":
            total_own += 1
        elif group["role"] == "Member":
            total_member += 1
        else:
            total_public += 1

        # Filter based on relation to group
        if only_owner:
            if group["role"] != "Owner":
                keep = False
        elif only_public:
            if group["role"] != "None":
                keep = False
        elif only_member:
            if group["role"] != "Member":
                keep = False

        if not keep:
            continue

        if group["role"] == "Owner":
            total_filtered_own += 1
        elif group["role"] == "Member":
            total_filtered_member += 1
        else:
            total_filtered_public += 1

        group["createdate"] = datetime.datetime.fromtimestamp(
            group["createdate"] / 1000
        )
        group["member_count"] = group["memcount"] - 1

        filtered_groups.append(group)

    totals = {
        "all": len(groups),
        "own": total_own,
        "member": total_member,
        "public": total_public,
        "filtered": {
            "all": len(filtered_groups),
            "own": total_filtered_own,
            "member": total_filtered_member,
            "public": total_filtered_public,
        },
    }
    return filtered_groups, totals


def get_group(request, group_id):
    auth_token = request.kbase["auth"]["token"]
    groups_service = RESTClient(
        url=f"{base_url}/services/groups",
        token=auth_token,
        timeout=60,
    )

    group = groups_service.get(f"group/{group_id}")
    group["member_count"] = group["memcount"] - 1

    group["hidden_member_count"] = group["member_count"] - len(group["members"])

    return group


def wrapper(request, fun):
    if "error" in request.kbase:
        print("errrr", request.kbase["error"])
        return render(
            request,
            "error/index.html",
            {
                "page": {"title": "Error"},
                "error": request.kbase["error"],
                "kbase": request.kbase,
                "request": request,
            },
        )

    # Determine current tab
    try:
        return fun()

    except Exception as ex:
        print("ex", ex)
        return render(
            request,
            "error/index.html",
            {
                "page": {"title": "Error"},
                "error": {"message": str(ex)},
                "kbase": request.kbase,
                "request": request,
            },
        )


def get_selected_group(request, groups, id):
    selected_group = None
    if len(groups) == 0:
        selected_group = None
    elif id is None:
        selected_group = get_group(request, groups[0]["id"])
    else:
        if id in [x["id"] for x in groups]:
            selected_group = get_group(request, id)
        else:
            selected_group = get_group(request, groups[0]["id"])
    return selected_group


def index(request, id=None):
    def fun():
        query = request.GET.get("query")
        groups, totals = get_groups(request, query=query)

        # Get org detail if needed
        selected_group = get_selected_group(request, groups, id)

        return render(
            request,
            "orgs/index.html",
            {
                "page": {"title": "Orgs"},
                "kbase": request.kbase,
                "totals": totals,
                "groups": groups,
                "params": request.GET,
                "selected_group": selected_group,
                "request": request,
                "query": query,
                "tab": "index",
            },
        )

    return wrapper(request, fun)


def own(request, id=None):
    def fun():
        query = request.GET.get("query")
        groups, totals = get_groups(request, query=query, only_owner=True)

        # Get org detail if needed
        selected_group = get_selected_group(request, groups, id)

        return render(
            request,
            "orgs/index.html",
            {
                "page": {"title": "Orgs"},
                "kbase": request.kbase,
                "totals": totals,
                "groups": groups,
                "params": request.GET,
                "selected_group": selected_group,
                "query": query,
                "tab": "own",
            },
        )

    return wrapper(request, fun)


def member(request, id=None):
    def fun():
        query = request.GET.get("query")
        groups, totals = get_groups(request, query=query, only_member=True)

        # Get org detail if needed
        selected_group = get_selected_group(request, groups, id)

        return render(
            request,
            "orgs/index.html",
            {
                "page": {"title": "Orgs"},
                "kbase": request.kbase,
                "totals": totals,
                "groups": groups,
                "params": request.GET,
                "selected_group": selected_group,
                "query": query,
                "tab": "member",
            },
        )

    return wrapper(request, fun)


def public(request, id=None):
    def fun():
        query = request.GET.get("query")
        groups, totals = get_groups(request, query=query, only_public=True)

        # Get org detail if needed
        selected_group = get_selected_group(request, groups, id)

        return render(
            request,
            "orgs/index.html",
            {
                "page": {"title": "Orgs"},
                "kbase": request.kbase,
                "totals": totals,
                "groups": groups,
                "params": request.GET,
                "selected_group": selected_group,
                "query": query,
                "tab": "public",
            },
        )

    return wrapper(request, fun)
