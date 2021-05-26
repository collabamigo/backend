from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Teacher, Skill


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='email.email')

    class Meta:
        model = Profile
        fields = ('First_Name', 'Last_Name', 'Gender',
                  'Degree', 'Course', 'email', 'Handle', 'IsTeacher',
                  'Created', 'id')


class TeacherSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='email.email')
    skills = serializers.SerializerMethodField()

    def get_skills(self, obj):
        return obj.skills.values_list(flat=True)

    class Meta:
        model = Teacher
        fields = ['id', 'Contact', 'UpVotes', 'DownVotes', 'Gitname',
                  'Linkedin', 'email', 'skills', ]


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ('name', 'Teacher_set')


class UserSerializer(serializers.ModelSerializer):
    profile = serializers.PrimaryKeyRelatedField(
        queryset=Profile.objects.all()
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile']
