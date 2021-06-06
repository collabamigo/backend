import json
from Cryptodome.Random import random
from rest_framework.request import Request
from rest_framework.response import Response

from backend import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.forms.models import model_to_dict
from rest_framework.exceptions import ParseError, NotFound

from .models import Profile, Teacher, Skill, SkillSet
from rest_framework import viewsets, views, permissions, status
from .permissions import IsOwner, IsAdminOrReadOnlyIfAuthenticated
from .serializers import (ProfileSerializer,
                          TeacherSerializer, SkillSerializer)
from .emailhandler import send_mail
from . import email_templates, logger


def teachersdata(request):
    teachers = json.loads(request.GET.get('id_list'))
    output = []
    for k in teachers:
        profile = Profile.objects.get(id=str(k))
        profile_dict = model_to_dict(profile)
        try:
            teacher_dict = model_to_dict(profile.teacher)
        except Profile.teacher.RelatedObjectDoesNotExist:
            continue
        profile_dict.update(teacher_dict)
        allowed_fields = ['id', 'First_Name', 'Last_Name', 'degree', 'course',
                          'UpVotes', 'DownVotes', 'Gitname', 'Linkedin']
        result_dict = {key: profile_dict[key] for key in allowed_fields}
        output.append(result_dict)
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

    # TODO: Better id extraction

    def get_roll_number(self, em, deg):
        output = ""
        for i in em:
            if '0' <= i <= '9':
                output += i
            if i == "@":
                break
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
            request_id = logger.request_connection(student=str(student.id),
                                                   teacher=str(teacher.id),
                                                   skills=skills)
            if request_id == "THROTTLED":
                return Response("THROTTLED",
                                status=status.HTTP_429_TOO_MANY_REQUESTS)
            elif request_id == "BLOCKED":
                return Response("BLOCKED",
                                status=status.HTTP_403_FORBIDDEN)

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
        else:
            raise ParseError()


class ConnectionApprove(views.APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        identifier = str(random.randint(0, 70)) + ": "
        print(identifier + "post called on ConnectionApprove", flush=True)
        if 'request_id' in request.data and 'mobile' in request.data:
            obj = logger.accept_connection(request.data['request_id'])
            if not obj:
                raise ParseError()
            if obj['approvedAt']:
                return Response("Already approved",
                                status=status.HTTP_208_ALREADY_REPORTED)
            print(identifier + "valid request", flush=True)
            student = Profile.objects.get(id=obj['student'])
            teacher = Profile.objects.get(id=obj['teacher'])
            contact_details = {
                # 'Handle': teacher.handle,
                'Email ID': str(teacher.email.email),
                'LinkedIn': str(teacher.teacher.Linkedin),
                'Github page': str(teacher.teacher.Gitname),
            }
            if int(request.data['mobile']) == 1:
                contact_details['Mobile number'] = str(teacher.teacher.Contact)

            format_dict = {
                "teacherName": teacher.First_Name + " " + teacher.Last_Name,
                "contact": "",
                "receiverName": student.First_Name + " " + student.Last_Name,
            }
            for key in contact_details:
                format_dict['contact'] += str(key) + ": " + \
                                          contact_details[key] + "\n"
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
                      format(**format_dict), )
            return Response("Success", status=status.HTTP_200_OK)
        else:
            raise ParseError()


class ApprovalsView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request):
        if request.user.is_staff:
            student_id = str(request.query_params['id'])
        else:
            student_id = str(request.user.profile.id)
        approved_teachers = logger.list_approvals(student_id)
        return JsonResponse(approved_teachers, safe=False)


class PopularSkills(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request):
        return Response(list(map(str, sorted(Skill.objects.all(),
                                 key=lambda x: len(x.Teacher_set.values_list(
                                  flat=True)), reverse=True))))
