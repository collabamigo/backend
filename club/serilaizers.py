from rest_framework import serializers
from .models import Club, Competition, Social, Entry


class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = ('id', 'name', 'link', 'picture', 'college', 'join_date')
        read_only_fields = ['id', 'name', 'link', 'picture', 'college',
                            'join_date']


class CompetitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competition
        fields = ('id', 'club', 'on_going',)
        read_only_fields = ('id', 'club', 'on_going',)


class SocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Social
        fields = ("id", "club", "instagram", "linkedin", "facebook",
                  "discord", "other")
        read_only_fields = ("id", "club", "instagram", "linkedin", "facebook",
                            "discord", "other")


class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = ('id', 'participant', 'competition')
        read_only_fields = ('id', 'participant', 'competition')
