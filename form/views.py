# from django.shortcuts import render
from rest_framework import viewsets
# from rest_framework.response import Response
# from rest_framework import status
# from connect.permissions import IsAdminOrReadOnlyIfAuthenticated
from .models import Form
# Response as Res, FileResponse, TextResponse
from .serializers import FormSerializer


class FormView(viewsets.ModelViewSet):
    # permission_classes = [IsAdminOrReadOnlyIfAuthenticated]
    queryset = Form.objects.all()
    serializer_class = FormSerializer

