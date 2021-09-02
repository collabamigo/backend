from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework.request import Request
import jwt
from Cryptodome.Hash import SHA512

from .models import RefreshToken


class CustomAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request: Request):
        if 'Authorization' in request.headers and request.headers['Authorization'].startswith("Token"):
            jwt_payload = jwt.decode(request.headers["Authorization"].split()[1], settings.JWT_SECRET,
                                     algorithms=["HS256"])

            user = User.objects.get(email=jwt_payload.get("email"))
            hasher = SHA512.new(truncate="256")
            token = RefreshToken.objects.get(token__user=user)
            hasher.update(token.token.key.encode('utf-8'))

            if jwt_payload.get(
                    "hash") == hasher.hexdigest() and datetime.now() < datetime.fromtimestamp(jwt_payload['exp']):
                print(request.method+" request received on " +
                      request.path+" by "+jwt_payload['email'] +
                      " with data "+str(request.query_params),
                      flush=True)
                return user, None
            else:
                print("Credential verification failed", flush=True)
        return None
