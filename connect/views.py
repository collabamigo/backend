import json
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.forms.models import model_to_dict
from .models import Profile, Teacher, Skill
from rest_framework import viewsets
from .permissions import IsOwner, IsAdminOrReadOnlyIfAuthenticated
from .serializers import (ProfileSerializer,
                          TeacherSerializer, SkillSerializer)
from .emailhandler import registration_email


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
    permission_classes = [IsOwner]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
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
        email = str(self.request.user.email)
        deg = self.request.data["degree"]
        id_ = self.get_roll_number(email, deg)
        person = {
            "Id": id_,
            "Name": self.request.data["First_Name"] + " " +
            self.request.data["Last_Name"],
            "Email": email
        }
        registration_email(person)
        serializer.save(email=self.request.user,
                        id=id_)


@method_decorator(csrf_exempt, name='dispatch')
class TeacherView(viewsets.ModelViewSet):
    permission_classes = [IsOwner]
    serializer_class = TeacherSerializer
    queryset = Teacher.objects.all()

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Teacher.objects.all()
        else:
            return Teacher.objects.filter(email=user)

# TODO: V2 Better get_roll_number implementation needed

    def get_roll_number(self):
        x = str(self.id)
        output = ""
        for i in x:
            if i == 'B' or i == 'M':
                output += i
            if '0' <= i <= '9':
                output += i
        return output

    def perform_create(self, serializer):
        iid = self.get_roll_number()
        b = Profile.objects.get(id=iid)
        b.IsTeacher = True
        print(iid, flush=True)
        print(b.IsTeacher, flush=True)
        b.save()
        serializer.save(email=self.request.user,
                        id=self.request.user.profile)


@method_decorator(csrf_exempt, name='dispatch')
class SkillView(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnlyIfAuthenticated]
    serializer_class = SkillSerializer
    queryset = Skill.objects.all()

    def get_queryset(self):
        if self.action == "retrieve" or self.request.user.is_staff:
            return Skill.objects.all()
        else:
            return Skill.objects.none()
