from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from .models import Club, Competition, Announcement


class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = ('id', 'name', 'picture', 'college', 'join_date',
                  'instagram', 'linkedin', 'facebook', 'discord', 'other',
                  'username', 'memberSize', 'tagline', 'description',
                  'announcements', 'competitions', 'admins')
        read_only_fields = ['id', 'name', 'picture', 'college',
                            'join_date', 'username', 'announcements', 'competitions', 'admins']


class CompetitionSerializer(serializers.ModelSerializer):
    clubs = SlugRelatedField(allow_empty=False, many=True,
                             queryset=Club.objects.all(), slug_field='username')

    class Meta:
        model = Competition
        fields = "__all__"
        read_only_fields = ['id']


class AnnouncementsSerializer(serializers.ModelSerializer):
    club = SlugRelatedField(allow_empty=False, queryset=Club.objects.all(),
                            slug_field='username')

    class Meta:
        model = Announcement
        fields = '__all__'
        read_only_fields = ['id', 'timestamp']
