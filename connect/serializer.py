from rest_framework import serializers

from . models import *


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('id', 'title', 'description', 'completed')


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('id', 'fist_name', 'last_name', 'age', 'gender',
                  'education', 'email;', 'contact', 'handle', 'isvendor')


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('id', 'Skill_set')


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('id', 'Teacher_set')
