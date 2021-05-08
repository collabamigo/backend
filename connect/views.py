from .models import Todo, Profile, Teacher, Skill
from rest_framework import viewsets
# from rest_framework.views import APIView
# from rest_framework.response import Response
from .serializer import (TodoSerializer, ProfileSerializer,
                         TeacherSerializer, SkillSerializer,
                         TodoSerializer2)


class TodoView(viewsets.ModelViewSet):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()


class TodoView2(viewsets.ModelViewSet):
    serializer_class = TodoSerializer2
    queryset = Todo.objects.all()


class ProfileView(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()


# class ProfileView2(viewsets.ModelViewSet):
#     serializer_class = ProfileSerializer2
#     queryset = Profile.objects.get(id="B2020064")


class TeacherView(viewsets.ModelViewSet):
    serializer_class = TeacherSerializer
    queryset = Teacher.objects.all()


class SkillView(viewsets.ModelViewSet):
    serializer_class = SkillSerializer
    queryset = Skill.objects.all()
