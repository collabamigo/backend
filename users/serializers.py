from abc import ABC

from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import UserDevice


class UserDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDevice
        fields = "__all__"


class NameEmailSerializer(serializers.ModelSerializer):
    class NameField(serializers.RelatedField, ABC):
        def to_representation(self, value):
            return value.First_Name + " " + value.Last_Name

    name = NameField(read_only=True, source="profile")

    class Meta:
        model = get_user_model()
        fields = ['email', 'name']
        read_only_fields = ['email', ]
