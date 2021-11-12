from rest_framework import serializers
from .models import Club, Competition, Announcement


class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = ('id', 'name', 'picture', 'college', 'join_date',
                  'instagram', 'linkedin', 'facebook', 'discord', 'other',
                  'username', 'memberSize', 'tagline', 'description')
        read_only_fields = ['id', 'name', 'picture', 'college',
                            'join_date', 'instagram', 'linkedin',
                            'facebook', 'discord', 'other', 'username']


class CompetitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competition
        fields = ('id', 'club', 'name', 'description', 'on_going', 'disabled')
        read_only_fields = ['id']


class AnnouncementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ('id', 'content', 'announcements')
