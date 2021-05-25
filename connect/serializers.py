from rest_framework import serializers
from .models import Profile, Teacher, Skill


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='email.email')

    class Meta:
        model = Profile
        fields = ['First_Name', 'Last_Name', 'Gender',
                  'Degree', 'Course', 'email', 'Handle', 'IsTeacher',
                  'Created', ]


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'Contact', 'UpVotes', 'DownVotes', ]
        read_only_fields = ['UpVotes', 'DownVotes']


class SkillSerializer(serializers.ModelSerializer):

    class Meta:
        model = Skill
        fields = ['name', 'Teacher_set', ]
