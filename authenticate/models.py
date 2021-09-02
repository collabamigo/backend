from datetime import timedelta, datetime

from rest_framework.authtoken.models import Token
from django.db import models

from backend.settings import TOKEN_VALIDITY_IN_DAYS


class RefreshToken(models.Model):
    token = models.OneToOneField(Token, on_delete=models.CASCADE)
    expiry = \
        models.DateTimeField(default=lambda: datetime.now() + timedelta(
                                                 days=TOKEN_VALIDITY_IN_DAYS))
