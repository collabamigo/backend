from rest_framework import serializers
from .models import Idea


class IdeaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Idea
        fields = ("id", "name", "profile", "idea", "visibility",
                  "estimate_time", "team_size", "tags", "stage", "college",
                  "join_date")
