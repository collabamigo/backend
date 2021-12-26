from datetime import datetime, timedelta
from secrets import choice
import string
from django.http import JsonResponse
from backend.settings import User
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework import status
from rest_framework.views import APIView

from backend import settings
from .utils import verify_token, create_firebase_token
from . import models
import jwt
from Cryptodome.Hash import SHA512
from django.contrib.auth import get_user_model


class RandomUsername:
    """
    using firstname & lastname
    create a random username (all lower case)
    that doesnt already exist in db
    """
    num_of_random_letters = 3
    num_of_random_numbers = 2
    user_model = get_user_model()

    def get_username(self, slug: str = None):
        username = ''
        if slug:
            username = slug

        while True:
            random_letters = string.ascii_lowercase
            random_numbers = string.digits
            username += self.get_random_char(
                random_letters, self.num_of_random_letters
            )
            username += self.get_random_char(
                random_numbers, self.num_of_random_numbers
            )
            if self.username_exist_in_db(username) is False:
                return username

    def username_exist_in_db(self, username):
        """
        :return: True if username already exist in db
            else False
        """
        q = self.user_model.objects.filter(username=username)
        return q.exists()

    def get_random_char(self, ip_str, n):
        return (''.join(
            choice(ip_str)
            for _ in range(n)
        ))


class OAuthCallback(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request: Request):

        email, picture = verify_token(request.data.get("jwt"))
        if email:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                username = RandomUsername().get_username(slug=email.split("@")[0])
                user = User.objects.create_user(
                        username=username, email=email, first_name=picture)
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
            return JsonResponse(data={}, status=status.HTTP_401_UNAUTHORIZED)


class RefreshJWT(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

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


class GetFirebaseToken(APIView):
    def get(self, request: Request):
        return JsonResponse(
            {
                'firebaseToken': create_firebase_token(request.user)
            }
        )
