
from rest_framework import viewsets
from .models import Form, Response
from .serializers import FormSerializer, ResponseSerializer


class FormView(viewsets.ModelViewSet):
    # permission_classes = [IsAdminOrReadOnlyIfAuthenticated]
    queryset = Form.objects.all()
    serializer_class = FormSerializer
    lookup_field = 'competition_id'


class ResponseView(viewsets.ModelViewSet):
    queryset = Response.objects.all()
    serializer_class = ResponseSerializer
