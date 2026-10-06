from django.conf import settings


def set_auth_cookies(response, access, refresh):
    secure = not settings.DEBUG
    common = {
        "httponly": True,
        "secure": secure,
        "samesite": "Lax",
        "path": "/",
    }
    response.set_cookie("jobflow_access", access, max_age=60 * 60, **common)
    response.set_cookie("jobflow_refresh", refresh, max_age=60 * 60 * 24 * 7, **common)
    return response


def clear_auth_cookies(response):
    response.delete_cookie("jobflow_access", path="/")
    response.delete_cookie("jobflow_refresh", path="/")
    return response
