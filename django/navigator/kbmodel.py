from django.conf import settings
from lib.GenericClient2 import GenericClient2
from datetime import datetime
from dateutil.parser import parse
import time
from concurrent.futures import ThreadPoolExecutor
import re
import json

# class NavigatorModel(object):
#     def __init__(self):
#         self.token =

SEARCHAPI_URL = settings.KBASE["services"]["search"]["url"]
AUTH_URL = settings.KBASE["services"]["auth"]["url"]


def get_narrative_totals(auth_token, owner):
    def fetcher(filter):
        return get_narratives_total(filter, auth_token, owner, offset=0, limit=0)[0]

    pool = ThreadPoolExecutor(max_workers=5)

    filters = ["own", "shared", "public", "tutorial"]

    start = time.time()
    totals = {}
    for (index, result) in enumerate(pool.map(fetcher, filters)):
        totals[filters[index]] = result
    print("elapsed", time.time() - start)

    return totals


def filter_to_query(filter, owner):
    query = {"bool": {"must": [], "must_not": [{"term": {"is_temporary": True}}]}}
    if filter == "own":
        query["bool"]["must"].append({"term": {"owner": owner}})
    elif filter == "shared":
        query["bool"]["must"].append({"term": {"shared_users": owner}})
        query["bool"]["must_not"].append({"term": {"owner": owner}})
    elif filter == "tutorial":
        query["bool"]["must"].append({"term": {"is_narratorial": True}})
        query["bool"]["must_not"].append({"term": {"owner": owner}})
    elif filter == "public":
        query["bool"]["must"].append({"term": {"is_public": True}})
        query["bool"]["must_not"].append({"term": {"owner": owner}})
    return query


def get_narratives(filter, auth_token, owner, offset=0, limit=1000):
    client = GenericClient2(
        url=SEARCHAPI_URL, module=None, token=auth_token, timeout=60
    )
    query = filter_to_query(filter, owner)
    try:
        result = client.call_func(
            "search_objects",
            {
                "query": query,
                "from": offset,
                "size": limit,
                "indexes": ["narrative"],
                "sort": [{"timestamp": {"order": "desc"}}, "_score"],
                "track_total_hits": True,
            },
        )
    except Exception as e:
        return None, {"exception": e, "message": str(e)}

    # Okay, format the data into something friendlier; also, we can
    # handle transforming in Python rather than in the template.

    narratives = []
    for hit in result["hits"]:
        doc = hit["doc"]
        created_at = parse(doc["creation_date"])
        modified_at = datetime.fromtimestamp(hit["doc"]["modified_at"] / 1000.0)
        narratives.append(
            {
                "id": doc["access_group"],
                "title": doc["narrative_title"],
                "owner": doc["owner"],
                "created_at": created_at.strftime("%Y-%m-%d"),
                "modified_at": modified_at.strftime("%Y-%m-%d"),
                "cell_count": len(doc["cells"]),
                "object_count": len(doc["data_objects"]),
                "version": doc["version"],
                "is_public": doc["is_public"],
            }
        )

    return {"total_count": result["count"], "narratives": narratives}


def get_narrative(id, auth_token, owner):
    client = GenericClient2(
        url=SEARCHAPI_URL, module=None, token=auth_token, timeout=60
    )
    query = {"bool": {"must": [{"term": {"access_group": id}}]}}
    # try:
    result = client.call_func(
        "search_objects",
        {
            "query": query,
            "from": 0,
            "size": 1,
            "indexes": ["narrative"],
            "track_total_hits": True,
        },
    )
    # except Exception as e:
    #     return {"exception": e, "message": str(e)}

    # Okay, format the data into something friendlier; also, we can
    # handle transforming in Python rather than in the template.

    for hit in result["hits"]:
        doc = hit["doc"]
        created_at = parse(doc["creation_date"])
        modified_at = datetime.fromtimestamp(hit["doc"]["modified_at"] / 1000.0)

        object_type_counts = {}
        objects = []
        for obj in doc["data_objects"]:
            module_name, type_name, ver_major, ver_minor = re.split(
                "[.-]", obj["obj_type"]
            )
            if type_name in object_type_counts:
                object_type_counts[type_name] += 1
            else:
                object_type_counts[type_name] = 1
            objects.append(
                {
                    "type": {
                        "id": obj["obj_type"],
                        "module": module_name,
                        "name": type_name,
                        "version_major": ver_major,
                        "version_minor": ver_minor,
                    },
                    "name": obj["name"],
                }
            )
        data_object_counts = [
            [key, value] for (key, value) in object_type_counts.items()
        ]

        cell_type_counts = {}
        for cell in doc["cells"]:
            cell_type = cell["cell_type"]
            if cell_type in cell_type_counts:
                cell_type_counts[cell_type] += 1
            else:
                cell_type_counts[cell_type] = 1
        cell_counts = [[key, value] for (key, value) in cell_type_counts.items()]

        # print("cells?", doc["cells"], json.dumps(doc))

        return {
            "id": doc["access_group"],
            "title": doc["narrative_title"],
            "owner": doc["owner"],
            "author": doc["creator"],
            "created_at": created_at.strftime("%Y-%m-%d"),
            "modified_at": modified_at.strftime("%Y-%m-%d"),
            "cell_count": len(doc["cells"]),
            "object_count": len(doc["data_objects"]),
            "version": doc["version"],
            "shared_users": doc["shared_users"],
            "cells": doc["cells"],
            "cell_counts": cell_counts,
            "data_objects": objects,
            "data_object_counts": data_object_counts,
            "is_public": doc["is_public"],
        }


def get_narratives_total(filter, auth_token, owner, offset=0, limit=1000):
    client = GenericClient2(
        url=SEARCHAPI_URL, module=None, token=auth_token, timeout=60
    )
    query = filter_to_query(filter, owner)
    try:
        result = client.call_func(
            "search_objects",
            {
                "query": query,
                "from": 0,
                "size": 0,
                "indexes": ["narrative"],
                "track_total_hits": True,
            },
        )
    except Exception as e:
        return None, {"exception": e, "message": str(e)}

    # Okay, format the data into something friendlier; also, we can
    # handle transforming in Python rather than in the template.

    return result["count"], None
