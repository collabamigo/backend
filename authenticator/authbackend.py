from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import authentication
from authenticator import AuthHandler


ALLOWED_IN_DEBUG = ['adityapratapsingh51@gmail.com',
                    'aditya20016@iiitd.ac.in', 'shikhar20121@iiitd.ac.in',
                    'heemank20064@iiitd.ac.in', 'heemankv@gmail.com']


class CustomAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        if 'aeskey' in request.headers and "iv" in request.headers and \
                "token" in request.headers:
            try:
                auth, img = AuthHandler.authenticate(
                    request.headers['token'],
                    request.headers['aeskey'],
                    request.headers['iv'])

            except ValueError:
                print("Internal error encountered in "
                      "AuthHandler authentication",
                      flush=True)
                auth = ""
            if auth and (not settings.DEBUG or auth in ALLOWED_IN_DEBUG):
                username = auth.split("@")[0]
                try:
                    user = User.objects.get(username=username)
                except User.DoesNotExist:
                    user = User(username=username, email=auth, first_name=img)
                    user.is_staff = False
                    user.is_superuser = False
                    user.save()
                return user, None
            else:
                print("Credential verification failed", flush=True)
        return None
