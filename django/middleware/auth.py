from lib.RESTClient import RESTError
from django.conf import settings

from lib.GenericClient import GenericClient
from lib.RESTClient import RESTClient

TOKEN_COOKIE_NAME = "kbase_session"


def simple_middleware(get_response):
    def middleware(request):
        #
        # Do stuff before
        #

        auth_token = request.COOKIES.get("kbase_session")

        request.kbase = {"auth": {"token": auth_token}, "settings": settings.KBASE}

        if auth_token is not None:
            auth_url = settings.KBASE["services"]["auth"]["url"]
            authService = RESTClient(url=auth_url, timeout=60, token=auth_token)
            try:
                me = authService.get("api/V2/me")
            except RESTError as re:
                request.kbase["is_authenticated"] = False
                request.kbase["error"] = {"message": re.message}
                print("ERROR", re.message)
            else:
                request.kbase["auth"]["me"] = me
                user_profile_url = settings.KBASE["services"]["user_profile"]["url"]
                user_profile_service = GenericClient(
                    url=user_profile_url,
                    module="UserProfile",
                    token=auth_token,
                    timeout=60,
                )
                [user_profile] = user_profile_service.call_func(
                    "get_user_profile", [me["user"]]
                )
                request.kbase["auth"]["user_profile"] = user_profile
                request.kbase["is_authenticated"] = True
        else:
            request.kbase["is_authenticated"] = False

        #
        # Next middleware / handler
        #
        response = get_response(request)

        #
        # Do stuff after
        #

        return response

    return middleware
