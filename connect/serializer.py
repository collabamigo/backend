from rest_framework import serializers

from . models import Todo, Profile, Teacher, Skill


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('First_Name', 'Last_Name', 'Gender',
                  'Degree', 'Course', 'Handle', 'IsTeacher')


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('First_Name', 'Last_Name', 'Gender',
                  'Degree', 'Course', 'Email', 'Handle', 'IsTeacher')


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ('id', 'Skill_set', 'Contact')


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ('id', 'Teacher_set')
