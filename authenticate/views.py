from datetime import datetime, timedelta

from django.http import JsonResponse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.request import Request
from rest_framework import status
from rest_framework.views import APIView

from backend import settings
from .AuthHandler import verify_token
from . import models
import jwt
from Cryptodome.Hash import SHA512


class OAuthCallback(APIView):

    def post(self, request: Request):

        email, picture = verify_token(request.data.get("jwt"))
        if email:
            username = email.split("@")[0]
            user = User.objects.get_or_create(email=email, username=username,
                                              first_name=picture)[0]
            Token.objects.filter(user=user).delete()
            token = Token.objects.create(user=user)
            refresh_token = models.RefreshToken.objects.create(token=token)
            hasher = SHA512.new(truncate="256")
            hasher.update(refresh_token.token.key.encode('utf-8'))
            jwt_payload = {"email": email, "hash": hasher.hexdigest(),
                           "exp": datetime.now() + timedelta(
                               days=settings.JWT_VALIDITY_IN_DAYS)}
            return JsonResponse(
                {"access_token": jwt.encode(payload=jwt_payload,
                                            key=settings.JWT_SECRET,
                                            algorithm="HS256"),
                 "refresh_token": refresh_token.token.key})

        else:
            return JsonResponse(data=request.data, status=status.HTTP_401_UNAUTHORIZED)


class RefreshJWT(APIView):

    def post(self, request: Request):
        refresh_token_by_user = request.POST.get("refresh_token")
        access_token = request.POST.get("access_token")
        if refresh_token_by_user and access_token:
            jwt_payload = jwt.decode(access_token, settings.JWT_SECRET, algorithms=["HS256"])
            user = User.objects.get(email=jwt_payload.get("email"))
            hasher = SHA512.new(truncate="256")
            token = models.RefreshToken.objects.get(token__user=user)
            hasher.update(token.token.key.encode('utf-8'))

            if jwt_payload.get(
                    "hash") == hasher.hexdigest() and \
                    token.token.key == refresh_token_by_user \
                    and datetime.now() < datetime.fromtimestamp(token.expiry):
                jwt_payload = {"email": jwt_payload.get("email"),
                               "hash": hasher.hexdigest(),
                               "exp": datetime.now() + timedelta(
                                   days=settings.JWT_VALIDITY_IN_DAYS)}
                return JsonResponse({"access_token": jwt.encode(
                    payload=jwt_payload, key=settings.JWT_SECRET, algorithm="HS256")})
            else:
                return JsonResponse({}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return JsonResponse({}, status=status.HTTP_400_BAD_REQUEST)
