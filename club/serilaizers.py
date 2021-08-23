
from rest_framework import serializers
from .models import Club, Competition


class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = ('id', 'name', 'link', 'picture', 'college', 'join_date')
        read_only_fields = ['id', 'name', 'link', 'picture', 'college',
                            'join_date']


class CompetitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competition
        fields = ('id', 'on_going',)
