from rest_framework import serializers

from connect.serializers import ProfileSerializer
from .models import Idea


class IdeaSerializer(serializers.ModelSerializer):
    owner_details = ProfileSerializer(read_only=True, source="owners", many=True)
    bookmarked_by = ProfileSerializer(read_only=True, many=True)

    class Meta:
        model = Idea
        fields = "__all__"
