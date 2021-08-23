from rest_framework import serializers
# from rest_framework.relations import PrimaryKeyRelatedField
from .models import Club, Competition, Entries


class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = ('id', 'name', 'link', 'picture', 'college', 'join_date')


class CompetitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competition
        fields = ('id', 'on_going',)
