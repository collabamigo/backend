import json
from rest_framework.response import Response
from backend import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.forms.models import model_to_dict
from rest_framework.exceptions import ParseError, NotFound

from .logger import request_connection, accept_connection
from .models import Profile, Teacher, Skill
from rest_framework import viewsets, views, permissions
from .permissions import IsOwner, IsAdminOrReadOnlyIfAuthenticated
from .serializers import (ProfileSerializer,
                          TeacherSerializer, SkillSerializer)
from .emailhandler import send_mail
from . import email_templates


def teachersdata(request):
    called_skills = json.loads(request.GET.get('id_list'))
    output = list()
    for k in called_skills:
        profile_object = model_to_dict(Profile.objects.get(id=str(k)))
        teacher_object = model_to_dict(Teacher.objects.get(id=str(k)))
        # TODO : try Profile.teacher instead of id calling
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
        return str(deg) + output

    def perform_create(self, serializer):
        email = str(self.request.user.email)
        deg = self.request.data["degree"]
        id_ = self.get_roll_number(email, deg)
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

    def perform_create(self, serializer):
        b = self.request.user.profile
        b.IsTeacher = True
        b.save()
        serializer.save(email=self.request.user,
                        id=self.request.user.profile)

    def perform_destroy(self, instance):
        b = self.request.user.profile
        b.IsTeacher = False
        b.save()
        return super().perform_destroy(instance)


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


class ConnectionRequest(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if 'id' in request.data and 'skills' in request.data and \
                request.data.get('id') != str(request.user.profile.id):
            teacher = None
            try:
                teacher = Profile.objects.get(id=request.data['id'])
            except Profile.DoesNotExist:
                raise NotFound()
            student = request.user.profile
            skills = request.data['skills']

            skill_store = teacher.teacher.skills.values_list(flat=True)
            for skill in skills:
                if skill not in skill_store:
                    raise ParseError()

            request_id = request_connection(student=str(student.id),
                                            teacher=str(teacher.id),
                                            skills=skills)
            url = 'https://collabconnect-development.firebaseapp.com/' if \
                settings.DEBUG else 'https://collabconnect.web.app/'
            url += '/connection/?request_id=' + request_id
            format_dict = {
                "buttonUrl": url,
                "senderName": student.First_Name + " " +
                student.Last_Name,
                "skillsAsStr": ", ".join(skills),
                "receiverName": teacher.First_Name + " " +
                teacher.Last_Name
            }
            if request.data.get("message"):
                format_dict['message'] = "Message from " + \
                                         format_dict['senderName'] + ": \n" + \
                                         request.data.get('message')
            else:
                format_dict['message'] = ''

            send_mail(to=[str(teacher.email.email)],
                      subject="CollabConnect Connection Request",
                      body=email_templates.connection_request_text.
                      format(**format_dict),
                      html=email_templates.connection_request_html.
                      format(**format_dict))
            return Response()

        elif 'request_id' in request.data and 'mobile' in request.data:
            obj = accept_connection(request.data['request_id'])
            if not obj:
                raise ParseError()
            student = Profile.objects.get(id=obj['student'])
            teacher = Profile.objects.get(id=obj['teacher'])
            contact_details = {
                'Handle': teacher.handle,
                'Email ID': str(teacher.email.email),
            }
            if int(request.data['mobile']) == 1:
                contact_details['Mobile number'] = teacher.teacher.Contact

            format_dict = {
                "teacherName": teacher.First_Name + " " + teacher.Last_Name,
                "contact": "",
                "receiverName": student.First_Name + " " + student.Last_Name,
            }
            for key in contact_details:
                format_dict['contact'] += str(key) + ": " + \
                                          contact_details[key] + "\n"

            send_mail(to=[str(student.email.email)],
                      subject="CollabConnect Connection Request Approval",
                      body=email_templates.connection_approval_text.
                      format(**format_dict), )
            return Response()
        else:
            raise ParseError()
