from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.relations import PrimaryKeyRelatedField

from club.serializers import ClubSerializer
from . import connection_manager
from .models import Profile, Teacher, Skill


def strip_username(data: str):
    if data.endswith("/"):
        data = data[:-1]
    if "/" in data:
        data = data.split("/")[-1]
    if data.startswith("@"):
        data = data.split[1:]
    print("Returning " + data, flush=True)
    return data


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='email.email')
    clubs = ClubSerializer(many=True, read_only=True, source='email.clubs')

    def validate_handle(self, value):
        return strip_username(value)

    class Meta:
        model = Profile
        fields = ['id', 'First_Name', 'Last_Name', 'gender',
                  'degree', 'course', 'email', 'handle', 'clubs']
        read_only_fields = ['id', 'email', 'clubs']


class TeacherSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='email.email')
    skills = PrimaryKeyRelatedField(many=True,
                                    queryset=Skill.objects.all())
    help_history = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    def validate_gitname(self, value):
        return strip_username(value)

    def validate_linkedin(self, value):
        return strip_username(value)

    class Meta:
        model = Teacher
        fields = ['id', 'Contact', 'UpVotes', 'DownVotes', 'Gitname',
                  'Linkedin', 'email', 'skills',
                  'Created', 'help_history', 'image']
        read_only_fields = ['UpVotes', 'DownVotes', 'id', 'email',
                            'Created', 'help_history', 'image', ]

    def get_help_history(self, obj: Teacher):
        return connection_manager.list_approvals_sent(str(obj.id))

    def get_image(self, obj: Teacher):
        return obj.email.first_name


class SkillSerializer(serializers.ModelSerializer):
    Teacher_set = PrimaryKeyRelatedField(many=True,
                                         queryset=Teacher.objects.all())

    class Meta:
        model = Skill
        fields = ('name', 'Teacher_set')


class UserSerializer(serializers.ModelSerializer):
    profile = serializers.PrimaryKeyRelatedField(
        queryset=Profile.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile']
