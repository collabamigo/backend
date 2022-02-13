import uuid

from Cryptodome.Random import random
from rest_framework.request import Request
from rest_framework.response import Response

from authenticate.authentication import PreSignupAuth, DummyAuthentication
from backend import settings
from django.http import JsonResponse
from django.forms.models import model_to_dict
from rest_framework.exceptions import ParseError, NotFound

from .models import Profile, Teacher, Skill, SkillSet
from rest_framework import viewsets, views, permissions, status
from .permissions import IsOwner, IsAdminOrReadOnlyIfAuthenticated
from .serializers import (ProfileClubSerializer,
                          TeacherSerializer, SkillSerializer)
from .emailhandler import send_mail
from . import email_templates, connection_manager


class TeachersData(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request):
        teachers = request.query_params.getlist('id_list[]')
        output = []
        for k in teachers:
            profile = Profile.objects.get(id=str(k))
            profile_dict = model_to_dict(profile)
            try:
                teacher_dict = model_to_dict(profile.teacher)
            except Profile.teacher.RelatedObjectDoesNotExist:
                continue
            profile_dict.update(teacher_dict)
            allowed_fields = ['id', 'First_Name', 'Last_Name', 'degree',
                              'course', 'Gitname', 'Linkedin']
            result_dict = {key: profile_dict[key] for key in allowed_fields}
            output.append(result_dict)
        return Response(output)


class ProfileView(viewsets.ModelViewSet):
    serializer_class = ProfileClubSerializer
    queryset = Profile.objects.all()
    permission_classes = [IsOwner]
    authentication_classes = [DummyAuthentication, PreSignupAuth]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Profile.objects.all()
        else:
            return Profile.objects.filter(email=user)

    def perform_create(self, serializer):
        id_ = str(uuid.uuid4().hex)
        serializer.save(email=self.request.user,
                        id=id_)


class TeacherView(viewsets.ModelViewSet):
    permission_classes = [IsOwner]
    serializer_class = TeacherSerializer
    queryset = Teacher.objects.all()

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Teacher.objects.all()
        else:
            return Teacher.objects.filter(email=user)

    def perform_create(self, serializer):
        serializer.save(email=self.request.user,
                        id=self.request.user.profile)


class SkillView(viewsets.ModelViewSet):
    lookup_value_regex = '[^/]+'
    permission_classes = [IsAdminOrReadOnlyIfAuthenticated]
    serializer_class = SkillSerializer
    queryset = Skill.objects.all()

    def get_queryset(self):
        if self.action == "retrieve" or self.request.user.is_superuser:
            return Skill.objects.all()
        else:
            return Skill.objects.none()


class ConnectionRequest(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if 'teacher_id' in request.data and 'skills' in request.data:
            teacher = None
            try:
                teacher = Profile.objects.get(id=request.data['teacher_id'])
            except Profile.DoesNotExist:
                raise NotFound()

            if request.user.is_superuser:
                student_id = str(request.query_params['id'])
            else:
                student_id = str(request.user.profile.id)

            if student_id == request.data['teacher_id']:
                return Response("SELF-CONNECTION NOT ALLOWED",
                                status=status.HTTP_403_FORBIDDEN)

            student = Profile.objects.get(id=student_id)
            skills = request.data['skills']

            skill_store = teacher.teacher.skills.values_list(flat=True)
            for skill in skills:
                if skill not in skill_store:
                    raise ParseError()
            request_id = connection_manager.request_connection(
                student=str(student.id),
                teacher=str(teacher.id),
                skills=skills)
            if request_id == "THROTTLED":
                return Response("THROTTLED",
                                status=status.HTTP_429_TOO_MANY_REQUESTS)
            elif request_id == "BLOCKED":
                return Response("BLOCKED",
                                status=status.HTTP_403_FORBIDDEN)

            url = 'https://collabamigo.xyz/' if \
                settings.DEVELOPMENT else 'https://collabamigo.com/'
            url += '/connection/?request_id=' + request_id
            format_dict = {
                "buttonUrl": url,
                "senderName":
                    student.First_Name + " " + student.Last_Name,
                "skillsAsStr": ", ".join(skills),
                "receiverName":
                    teacher.First_Name + " " + teacher.Last_Name,
                "frontend": settings.FRONTEND_URL
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
        else:
            raise ParseError()


class ConnectionApprove(views.APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        identifier = str(random.randint(0, 70)) + ": "
        print(identifier + "post called on ConnectionApprove", flush=True)
        if 'request_id' in request.data and 'mobile' in request.data:
            obj = connection_manager.accept_connection(
                request.data['request_id'])
            if not obj:
                raise ParseError()
            if obj['approvedAt']:
                return Response("Already approved",
                                status=status.HTTP_208_ALREADY_REPORTED)
            print(identifier + "valid request", flush=True)
            student = Profile.objects.get(id=obj['student'])
            teacher = Profile.objects.get(id=obj['teacher'])

            format_dict = {
                "teacherName": teacher.First_Name + " " + teacher.Last_Name,
                "teacherEmailId": teacher.email.email,
                "teacherTelegram": teacher.handle,
                "receiverName": student.First_Name + " " + student.Last_Name,
                "optionalMobile": "",
                "optionalMobileHtml": "",
                "frontend": settings.FRONTEND_URL
            }

            if int(request.data['mobile']) == 1 and \
                    str(teacher.teacher.Contact) != "0":
                format_dict['optionalMobile'] = str(teacher.teacher.Contact)
                format_dict['optionalMobileHtml'] = \
                    """<tr>
                    <td>Mobile number</td>
                    <td>""" + str(teacher.teacher.Contact) + \
                    """</td>
                    </tr>"""
            for skill in obj['skills']:
                skill_set = SkillSet.objects.get(teacher=teacher.teacher,
                                                 skill=Skill.objects.get(
                                                     name=skill))
                skill_set.approvals += 1
                skill_set.save()

            print(identifier + "Calling sendmail", flush=True)
            send_mail(to=[str(student.email.email)],
                      subject="CollabConnect Connection Request Approval",
                      body=email_templates.connection_approval_text.
                      format(**format_dict),
                      html=email_templates.connection_approval_html.
                      format(**format_dict))
            return Response("Success", status=status.HTTP_200_OK)
        else:
            raise ParseError()


class ApprovalsView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request):
        if request.user.is_superuser:
            student_id = str(request.query_params['id'])
        else:
            student_id = str(request.user.profile.id)
        approved_teachers = connection_manager.list_approvals_received(
            student_id)
        return JsonResponse(approved_teachers, safe=False)


class PopularSkills(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request):
        return Response(list(map(lambda x: {"name": x.name,
                                            "count": len(
                                                x.Teacher_set.values_list(
                                                    flat=True))},
                                 sorted(Skill.objects.all(),
                                        key=lambda x:
                                        len(x.Teacher_set.values_list(
                                            flat=True)), reverse=True)))[:5])
