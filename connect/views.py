from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework import generics, permissions
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from rest_framework.permissions import IsAdminUser

from .models import Todo, Profile, Teacher, Skill
from rest_framework import viewsets

from .permissions import IsOwner
from .serializers import (TodoSerializer, ProfileSerializer,
                          TeacherSerializer, SkillSerializer, UserSerializer)
from rest_framework.parsers import JSONParser
import json


@csrf_exempt
def Profilegetter(request):
    qm = (x for x in Profile.objects.get(email=request.user.email))
    output = ', '.join([q for q in qm])
    return JsonResponse(output, safe=False)


# TODO: RENAME THIS PLEASE
def teacheridsfor(request, search):
    skill = Skill.objects.get(name=search)
    output = list(map(lambda item: str(item), skill.Teacher_set.all().order_by(
        '-confidence',
        '-UpVotes',
        'DownVotes')))
    return JsonResponse(output, safe=False)


def teachersdata(request):
    calledskills = request.GET.get('id_list')
    calledskills = json.loads(calledskills)
    output = list()
    for k in calledskills:
        profileobject = model_to_dict(Profile.objects.get(id=str(k)))
        teacherobject = model_to_dict(Teacher.objects.get(id=str(k)))
        profileobject.update(teacherobject)
        output.append(profileobject)
    return JsonResponse(output, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class TodoView(viewsets.ModelViewSet):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()


@method_decorator(csrf_exempt, name='dispatch')
class ProfileView(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [
        permissions.IsAuthenticated,
        IsOwner, ]

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user = self.request.user
        if user.is_superuser:
            return Profile.objects.all()
        else:
            return Profile.objects.filter(email=user)

    def perform_create(self, serializer):
        serializer.save(email=self.request.user)


@method_decorator(csrf_exempt, name='dispatch')
class TeacherView(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = TeacherSerializer
    queryset = Teacher.objects.all()


@method_decorator(csrf_exempt, name='dispatch')
class SkillView(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = SkillSerializer
    queryset = Skill.objects.all()
