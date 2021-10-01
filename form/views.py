# from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from connect.permissions import IsAdminOrReadOnlyIfAuthenticated
from .models import Form
# Response as Res, FileResponse, TextResponse
from .serializers import FormSerializer


class FormView(viewsets.ModelViewSet):
    # permission_classes = [IsAdminOrReadOnlyIfAuthenticated]
    queryset = Form.objects.all()
    serializer_class = FormSerializer

    # def perform_create(self, serializer):
    #     queryset = Form.objects.all()
    #     if queryset.exists():
    #         return Response("Your response is already with us!",
    #                         status=status.HTTP_208_ALREADY_REPORTED)
    #     serializer.save()
