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


@csrf_exempt
def Profilegetter(request):
    qm = (x for x in Profile.objects.get(email=request.user.email))
    output = ', '.join([q for q in qm])
    return JsonResponse(output, safe=False)


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

    def get_roll_number(self):
        x = str(self.email)
        output = ""
        for i in x:
            if '0' <= i <= '9':
                output += i

        m = str(self.Degree) + output
        return m

    def perform_create(self, serializer):
        self.id = self.get_roll_number()
        person = {
            "Id": self.id,
            "Name": self.First_Name+" "+self.Last_Name,
            "Email": str((self.email).email)
        }
        registration_email(person)
        serializer.save(email=self.request.user)


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
