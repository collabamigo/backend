import json
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework import permissions
from django.forms.models import model_to_dict
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .models import Profile, Teacher, Skill
from rest_framework import viewsets
from .permissions import IsOwner
from .serializers import (ProfileSerializer,
                          TeacherSerializer, SkillSerializer)


def teachersdata(request):
    called_skills = request.GET.get('id_list')
    called_skills = json.loads(called_skills)
    output = list()
    for k in called_skills:
        profile_object = model_to_dict(Profile.objects.get(id=str(k)))
        teacher_object = model_to_dict(Teacher.objects.get(id=str(k)))
        profile_object.update(teacher_object)
        output.append(profile_object)
    return JsonResponse(output, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class ProfileView(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [
        permissions.IsAuthenticated,
        IsOwner]

    def get_queryset(self):
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
    permission_classes = [IsAuthenticated]
    serializer_class = SkillSerializer
    queryset = Skill.objects.all()
