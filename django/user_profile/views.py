from django.shortcuts import render
from django.conf import settings
from lib.GenericClient import GenericClient
from lib.RESTClient import RESTClient
import json
import time

silly_cache = {}

TOKEN = "TRRNVRPRRHPM3ZSN65XXVBYJX2M7JTQB"
TOKEN_USER = "eapearson"


def cache_it(key, value):
    silly_cache[key] = value


def is_cached(key):
    return key in silly_cache


def get_cache_entry(key):
    return silly_cache.get(key)


def maybe_get(key, fun):
    if key in silly_cache:
        return silly_cache[key]

    result = fun()
    silly_cache[key] = result
    return result


def fetch_profile(username, auth_token):
    user_profile_service = GenericClient(
        url=settings.KBASE["services"]["user_profile"]["url"],
        module="UserProfile",
        token=auth_token,
        timeout=60,
    )
    return user_profile_service.call_func("get_user_profile", [username])[0]


def fetch_organizations(username, auth_token):
    # A user profile wants to display the associated organizations.
    groups_service = RESTClient(
        url="{{ settings.service_base_url }}/services/groups",
        token=auth_token,
        timeout=60,
    )

    orgs, err = groups_service.get("member")

    # groups = len(orgs) / 100
    # groups_count = int(groups)
    # if groups > groups_count:
    #     groups_count += 1

    # all_groups = []
    # for groups_number in range(groups_count):
    #     groups_to_fetch = [org['id'] for org in orgs[groups_number:groups_number*100]]
    #     group_orgs, err = groups_service.get(f"group?groupids={','.join(groups_to_fetch)}")
    #     all_groups.extend(group_orgs)
    # return all_groups

    # print('orgs', user_organizations_list)

    # Now, for each org in the list, we need to get the org, then compare the
    # usernames in the membership fields to the subject user.
    organizations = []
    for org_item in orgs:
        org, err = groups_service.get(f"group/{org_item['id']}")
        organizations.append(org)
    return organizations


# Create your views here.
def index(request, username):
    auth_token = request.COOKIES.get("kbase_session")
    start = time.time()
    profile = fetch_profile(username, auth_token)
    print("profile", time.time() - start)
    start = time.time()

    userdata = profile["profile"]["userdata"]
    location = ", ".join(
        list(
            filter(
                lambda p: p is not None and p != "",
                [userdata.get("country"), userdata.get("state"), userdata.get("city")],
            )
        )
    )

    # orgs = fetch_organizations(username, auth_token)

    intersecting_orgs = []

    # for org in orgs:
    #     if username == org['owner'] or \
    #             len(list(filter(lambda u: u['name'] == username, org['admins']))) \
    #             or \
    #             len(list(filter(lambda u: u['name'] == username, org['members']))):
    #         intersecting_orgs.append(org)

    return render(
        request,
        "user_profile/index.html",
        {
            "page": {"title": f"{profile['user']['realname']} ({username})"},
            "profile": profile,
            "organizations": intersecting_orgs,
            "location": location,
            "kbase": request.kbase,
        },
    )
