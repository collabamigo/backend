from rest_framework import serializers
from .models import Club, Competition


class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = ('id', 'name', 'link', 'picture', 'college', 'join_date',
                  'instagram', 'linkedin', 'facebook', 'discord', 'other')
        read_only_fields = ['id', 'name', 'link', 'picture', 'college',
                            'join_date', 'instagram', 'linkedin',
                            'facebook', 'discord', 'other']


class CompetitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competition
        fields = ('id', 'club', 'name', 'description', 'on_going',)
        read_only_fields = ('id', 'name', 'description', 'club', 'on_going',)
