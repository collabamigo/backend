from abc import ABC

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from .models import Club, Competition, Announcement, CompetitionWinner

User = get_user_model()


class ClubSerializer(serializers.ModelSerializer):
    class AdminNameField(serializers.RelatedField, ABC):
        def to_representation(self, value):
            return value.profile.First_Name + " " + value.profile.Last_Name

    admins = AdminNameField(many=True, read_only=True)

    class Meta:
        model = Club
        fields = ('id', 'name', 'image_links', 'college', 'join_date',
                  'instagram', 'linkedin', 'facebook', 'discord', 'github', 'mail', 'telegram', 'youtube', 'other',
                  'username', 'memberSize', 'tagline', 'description',
                  'announcements', 'competitions', 'admins', 'medium')
        read_only_fields = ['id', 'name', 'college',
                            'join_date', 'username', 'announcements', 'competitions', 'admins']


class CompetitionWinnerSerializer(serializers.ModelSerializer):
    winner_first_name = serializers.CharField(source='winner.profile.First_Name', read_only=True)
    winner_last_name = serializers.CharField(source='winner.profile.Last_Name', read_only=True)
    winner_email = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='email', source='winner')

    class Meta:
        model = CompetitionWinner
        fields = ["position", "index", "competition", "winner_first_name", "winner_last_name", "winner_email"]
        read_only_fields = []
        extra_kwargs = {
            "winner_email": {
                "write_only": True
            }
        }


class CompetitionSerializer(serializers.ModelSerializer):
    clubs = SlugRelatedField(allow_empty=False, many=True,
                             queryset=Club.objects.all(), slug_field='username')
    winners = CompetitionWinnerSerializer(many=True, read_only=True, source='competitionwinner_set')
    club_names = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name', source='clubs')

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
