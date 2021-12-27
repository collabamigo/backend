import json

from django.db.models import QuerySet
from rest_framework import viewsets, generics
from rest_framework.exceptions import APIException
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
    return FormResponse.objects.filter(form=form, responders=user)


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
        return FormResponse.objects.filter(form__competition__id=competition_id)


class SubmitResponseView(APIView):

    def post(self, request: Request, event_id):
        form = Form.objects.get(competition_id=event_id)

        if form.opens_at > timezone.now() or form.closes_at < timezone.now():
            raise APIException('Form is not open for submissions')

        if not form.allow_multiple_submissions and _get_users_responses(form, request.user).exists():
            raise APIException('Multiple submissions are not allowed')

        form_response = FormResponse(form=form)

        skeleton = json.loads(form_response.form.skeleton)
        response_elements = []
        for key, value in request.data.items():
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
