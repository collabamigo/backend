from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Todo, Profile, Teacher, Skill


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('First_Name', 'Last_Name', 'Gender',
                  'Degree', 'Course', 'Email', 'Handle', 'IsTeacher')


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='email.email')

    class Meta:
        model = Profile
        fields = ('First_Name', 'Last_Name', 'Gender',
                  'Degree', 'Course', 'email', 'Handle', 'IsTeacher',
                  'Created', )


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ('id', 'Skill_set', 'Contact','UpVotes','DownVotes')


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ('id', 'Teacher_set')


class UserSerializer(serializers.ModelSerializer):
    profile = serializers.PrimaryKeyRelatedField(
        queryset=Profile.objects.all()
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile']
