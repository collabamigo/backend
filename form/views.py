import json

from django.db.models import QuerySet
from rest_framework import viewsets, generics
from rest_framework.exceptions import APIException, PermissionDenied
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from django.contrib.auth import get_user_model

from authenticate.permissions import IsTrulyAuthenticated
from club.models import Competition
from club.permissions import IsClubOwner
from club.serializers import CompetitionSerializer
from .models import Form, FormResponse, ResponseElement
from .serializers import FormSerializer, FormResponseSerializer

User = get_user_model()


def _get_users_responses(form: Form, user: User) -> QuerySet[FormResponse]:
    return FormResponse.objects.filter(form=form, responders=user).order_by("-timestamp")


class FormView(viewsets.ModelViewSet):
    # permission_classes = [IsAdminOrReadOnlyIfAuthenticated]
    queryset = Form.objects.all()
    serializer_class = FormSerializer
    lookup_field = 'competition_id'


class ResponseDisplayView(generics.ListAPIView):
    permission_classes = [IsClubOwner]
    serializer_class = FormResponseSerializer

    def get_queryset(self):
        competition_id = self.kwargs['competition_id']

        # Dirty permission check
        if not self.request.user.is_superuser:
            allowed = False
            clubs = self.request.user.club_coordinator_of.all()
            for club in clubs:
                if club.competitions.filter(id=competition_id).exists():
                    allowed = True
                    break
            if not allowed:
                raise PermissionDenied("You do not have permission to view this response.")

        return FormResponse.objects.filter(form__competition__id=competition_id)


class SubmitResponseView(APIView):

    def post(self, request: Request, event_id: int, submission_type: str):
        form = Form.objects.get(competition_id=event_id)

        if not form.competition.is_active:
            raise APIException("This competition is not active.")

        if submission_type == "existing":
            _get_users_responses(form, request.user)[0].delete()

        if form.opens_at > timezone.now() or form.closes_at < timezone.now():
            raise APIException('Form is not open for submissions')

        if not form.allow_multiple_submissions and _get_users_responses(form, request.user).exists():
            raise APIException('Multiple submissions are not allowed')

        form_response = FormResponse(form=form)

        skeleton = json.loads(form_response.form.skeleton)
        response_elements = []
        for key, value in request.data.items():
            if isinstance(value, list):
                value = json.dumps(value)
            if str(key) == str(skeleton[int(key)]["id"]):
                response_elements.append(ResponseElement(parent=form_response, question=key, value=value))
            else:
                raise APIException("Invalid form field" + key)

        form_response.save()
        form_response.responders.add(request.user)

        ResponseElement.objects.bulk_create(response_elements)
        return Response({"success": True})


class ParticipationHistoryView(APIView):
    permission_classes = [IsTrulyAuthenticated]

    def get(self, request: Request):
        competitions = Competition.objects.filter(form__responses__responders=request.user).distinct()
        return Response(CompetitionSerializer(competitions, many=True).data)


class SelfFormResponseAPIView(APIView):
    permission_classes = [IsTrulyAuthenticated]

    def get(self, request: Request, competition_id):
        try:
            form_responses = _get_users_responses(Form.objects.get(competition_id=competition_id), request.user)
            return Response(FormResponseSerializer(form_responses, many=True).data)
        except Form.DoesNotExist:
            return Response(status=406)


class getEmailsAPIView(APIView):
    permission_classes = [IsTrulyAuthenticated]

    def get(self, request: Request, competition_id):
        response_list = []
        response_queryset = FormResponse.objects.filter(form__competition_id=competition_id).\
            values('responders__email').distinct()
        for i in response_queryset:
            if i['responders__email']:
                response_list.append(i['responders__email'])
        return Response({"data": response_list})
