import json
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework import permissions
from django.forms.models import model_to_dict
from rest_framework.permissions import IsAuthenticated
from .models import Profile, Teacher, Skill
from rest_framework import viewsets
from .permissions import IsOwner
from .serializers import (ProfileSerializer,
                          TeacherSerializer, SkillSerializer)
from . emailhandler import registration_email, new_teacher_email


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

    def get_roll_number(self, em, deg):
        output = ""
        for i in em:
            if '0' <= i <= '9':
                output += i
        m = str(deg) + output
        return m

    def perform_create(self, serializer):
        emai = str(self.request.user.email)
        deg = self.request.data["Degree"]
        id_ = self.get_roll_number(emai, deg)
        person = {
            "Id": id_,
            "Name": self.request.data["First_Name"]+" " +
            self.request.data["Last_Name"],
            "Email": emai
        }
        registration_email(person)
        serializer.save(email=self.request.user,
                        id=id_)


@method_decorator(csrf_exempt, name='dispatch')
class TeacherView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated,
                          IsOwner]
    serializer_class = TeacherSerializer
    queryset = Teacher.objects.all()

    def perform_create(self, serializer):
        b = Profile.objects.get(id=self.id)
        b.IsTeacher = True
        person = {
            "Id": b.id,
            "Name": b.First_Name+" "+b.Last_Name,
            "Email": str((b.email).email)
        }
        b.lol()
        serializer.save(email=self.request.user)
        new_teacher_email(person)


@method_decorator(csrf_exempt, name='dispatch')
class SkillView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SkillSerializer
    queryset = Skill.objects.all()
