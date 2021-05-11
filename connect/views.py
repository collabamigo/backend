from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Todo, Profile, Teacher, Skill
from rest_framework import viewsets
from .serializer import(TodoSerializer, ProfileSerializer,
                        TeacherSerializer, SkillSerializer)


def detail(request, titlee):
    qm = (x for x in Todo.objects.filter(title=titlee)[::])
    output = ', '.join([q.description for q in qm])
    return JsonResponse(output, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class TodoView(viewsets.ModelViewSet):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()


@method_decorator(csrf_exempt, name='dispatch')
class ProfileView(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()


@method_decorator(csrf_exempt, name='dispatch')
class TeacherView(viewsets.ModelViewSet):
    serializer_class = TeacherSerializer
    queryset = Teacher.objects.all()


@method_decorator(csrf_exempt, name='dispatch')
class SkillView(viewsets.ModelViewSet):
    serializer_class = SkillSerializer
    queryset = Skill.objects.all()
