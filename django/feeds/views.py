from django.conf import settings
from lib.RESTClient import RESTClient
from django.shortcuts import render


def notification_object(notification):
    action = None
    object_url = None
    actor = notification["actor"]
    obj = notification["object"]
    targets = notification["target"]
    target = None
    message = None
    notification_type = None
    if obj["type"] == "group":
        notification_type = "organization_event"
        if len(targets) == 1:
            target = targets[0]

            if target["type"] == "workspace":
                action = "added workspace"
            elif target["type"] == "app":
                action = "added app"
            else:
                # If a request is by a user for themselves, it is a "join" request
                if len(targets) == 1 and actor["id"] == targets[0]["id"]:
                    action = "to join"
                    print("ok", actor, targets)
        object_url = (
            f'{settings.KBASE["ui_base_url"]}/orgs/{notification["object"]["id"]}'
        )
    elif obj["type"] == "admin":
        # An admin message?
        notification_type = "system_message"
        message = notification["context"]["text"]
    return {
        "notification": notification,
        "object_url": object_url,
        "action": action or "UNKNOWN",
        "target": target,
        "type": notification_type,
        "message": message,
    }


def index(request, id=None):
    feeds_service = RESTClient(
        url=settings.KBASE["services"]["feeds"]["url"],
        timeout=60,
        token=request.kbase["auth"]["token"],
    )

    feeds_response = feeds_service.get("/api/V1/notifications?seen=1")

    notifications = {}
    selected_id = id

    # Just absorb all feed items; sometimes the user feed is not
    # accurate, and our model in this app is to jumble all notifications
    # together.
    for feed_key, feed_info in feeds_response.items():
        feed = feed_info["feed"]
        if len(feed) == 0:
            continue
        for feed_notification in feed:
            notifications[feed_notification["id"]] = notification_object(
                feed_notification
            )

    # Now sort them by date into a list
    notifications_list = [n for n in notifications.values()]

    # TODO: sort

    selected_notification = None
    if len(notifications) > 0:
        if selected_id is None:
            selected_id = notifications_list[0]["notification"]["id"]
        selected_notification = notifications[selected_id]

    return render(
        request,
        "feeds/index.html",
        {
            "page": {"title": "Notifications | Feeds"},
            "notifications": notifications_list,
            "selected_notification": selected_notification,
            "kbase": request.kbase,
        },
    )


# def index(request, id=None):
#     feeds_service = RESTClient(
#         url=settings.KBASE["services"]["feeds"]["url"],
#         timeout=60,
#         token=request.kbase["auth"]["token"],
#     )

#     print("ID", id)

#     feeds_response = feeds_service.get("/api/V1/notifications?seen=1")

#     feeds = []
#     for key, value in feeds_response.items():
#         value["id"] = key
#         feeds.append(value)

#     print("FEEDS", feeds)

#     if id is not None:
#         selected_feed = feeds_service.get('/api/V1/notification/')

#     selected_feed = {"id": id}

#     # Fetch all notifications!

#     return render(
#         request,
#         "feeds/index.html",
#         {
#             "page": {"title": "Feeds"},
#             "feeds": feeds,
#             "selected_feed": selected_feed,
#             "kbase": request.kbase,
#         },
#     )


# Create your views here.
