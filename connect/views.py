from .models import Todo, Profile, Teacher, Skill
from rest_framework import viewsets
from django.http import HttpResponse

from .serializer import (TodoSerializer, ProfileSerializer,
                         TeacherSerializer, SkillSerializer)


def detail(request, titlee):
    latest_question_list = Todo.objects.get(title=titlee)
    output = ', '.join([q.description for q in latest_question_list])
    return HttpResponse(output)


def retrieve(self, request, *args, **kwargs):
    instance = self.get_object()
    serializer = self.get_serializer(instance)
    return Response(serializer.data)


class TodoView(viewsets.ModelViewSet):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()


class ProfileView(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()


class TeacherView(viewsets.ModelViewSet):
    serializer_class = TeacherSerializer
    queryset = Teacher.objects.all()


class SkillView(viewsets.ModelViewSet):
    serializer_class = SkillSerializer
    queryset = Skill.objects.all()
