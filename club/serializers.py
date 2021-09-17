from rest_framework import serializers
from .models import Club, Competition, Entry, Form


class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = ('id', 'name', 'link', 'picture', 'college', 'join_date')
        read_only_fields = ['id', 'name', 'link', 'picture', 'college',
                            'join_date']


class CompetitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competition
        fields = ('id', 'club', 'name', 'description', 'on_going',)
        read_only_fields = ('id', 'name', 'description', 'club', 'on_going',)


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


class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model: Form
        fields = ('id', "entries", "edit_after_submit" "confirmation_message",
                  "is_quiz", "allow_view_score", "createdAt",
                  "updatedAt", "collect_email")
        read_only_fields = ('id', 'entries', 'edit_after_submit',
                            'allow_view_score', 'createdAt', 'updatedAt')
