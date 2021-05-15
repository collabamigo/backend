from django.http import HttpResponse, HttpRequest

from . import AuthHandler


class HttpResponseUnauthorized(HttpResponse):
    status_code = 401


def simple_middleware(get_response):
    def middleware(request: HttpRequest):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        if request.user.is_superuser or request.path.startswith("/admin"):
            # Django admin logged in
            request.email = 'SUDO6969@SUDO.COM'
            response = get_response(request)
        elif 'aeskey' in request.headers and "iv" in request.headers and \
                "token" in request.headers:
            auth = AuthHandler.authenticate(request.headers['token'],
                                            request.headers['aeskey'],
                                            request.headers['iv'])
            if auth:
                request.email = auth
                response = get_response(request)
            else:
                response = HttpResponseUnauthorized("Invalid Credentials")
        else:
            response = HttpResponseUnauthorized("Invalid Credentials")

        # Code to be executed for each request/response after
        # the view is called.

        return response

    return middleware
