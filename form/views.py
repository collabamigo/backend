import json

from rest_framework import viewsets
from rest_framework.exceptions import APIException
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from .models import Form, FormResponse, ResponseElement
from .serializers import FormSerializer, ResponseSerializer


class FormView(viewsets.ModelViewSet):
    # permission_classes = [IsAdminOrReadOnlyIfAuthenticated]
    queryset = Form.objects.all()
    serializer_class = FormSerializer
    lookup_field = 'competition_id'


class ResponseView(viewsets.ModelViewSet):
    queryset = FormResponse.objects.all()
    serializer_class = ResponseSerializer


class SubmitResponseView(APIView):

    def post(self, request: Request, event_id):
        form_response = FormResponse(form=Form.objects.get(competition_id=event_id))

        if form_response.form.opens_at > timezone.now() or form_response.form.closes_at < timezone.now():
            raise APIException('Form is not open for submissions')

        if not form_response.form.allow_multiple_submissions and FormResponse.objects.filter(responders=request.user):
            raise APIException('Multiple submissions are not allowed')

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
