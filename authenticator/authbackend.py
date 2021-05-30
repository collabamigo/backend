from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions
from authenticator import AuthHandler


class CustomAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        if 'aeskey' in request.headers and "iv" in request.headers and \
                "token" in request.headers:
            try:
                auth = AuthHandler.authenticate(request.headers['token'],
                                                request.headers['aeskey'],
                                                request.headers['iv'])
            except ValueError:
                print("Internal error encountered in "
                      "AuthHandler authentication",
                      flush=True)
                auth = ""
            if auth:
                username = auth.split("@")[0]
                try:
                    user = User.objects.get(username=username)
                except User.DoesNotExist:
                    user = User(username=username, email=auth)
                    user.is_staff = False
                    user.is_superuser = False
                    user.save()
                return user, None
            else:
                print("Credential verification failed", flush=True)
                exceptions.AuthenticationFailed('Invalid credentials')
        return None
