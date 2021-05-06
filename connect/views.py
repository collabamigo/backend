from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render
from rest_framework import viewsets
from .serializer import *
from .models import *


class TodoView(viewsets.ModelViewSet):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()


class ProfileView(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Todo.objects.all()


class TeacherView(viewsets.ModelViewSet):
    serializer_class = TeacherSerializer
    queryset = Todo.objects.all()


class SkillView(viewsets.ModelViewSet):
    serializer_class = SkillSerializer
    queryset = Todo.objects.all()
