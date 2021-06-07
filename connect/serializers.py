from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.relations import PrimaryKeyRelatedField

from .models import Profile, Teacher, Skill


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='email.email')

    class Meta:
        model = Profile
        fields = ['id', 'First_Name', 'Last_Name', 'gender',
                  'degree', 'course', 'email', 'handle',]
        read_only_fields = ['id', 'email']


class TeacherSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='email.email')
    skills = PrimaryKeyRelatedField(many=True,
                                    queryset=Skill.objects.all())

    class Meta:
        model = Teacher
        fields = ['id', 'Contact', 'UpVotes', 'DownVotes', 'Gitname',
                  'Linkedin', 'email', 'skills',
                  'Created']
        read_only_fields = ['UpVotes', 'DownVotes', 'id', 'email',
                            'Created']


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
