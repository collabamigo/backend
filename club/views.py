# from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from connect.permissions import IsAdminOrReadOnlyIfAuthenticated
from .models import Club, Competition, Entry, Form
from .serializers import ClubSerializer, CompetitionSerializer, \
    EntrySerializer, FormSerializer


# Create your views here.

class ClubView(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnlyIfAuthenticated]
    queryset = Club.objects.all()
    serializer_class = ClubSerializer

    def perform_create(self, serializer):
        queryset = Club.objects.all()
        if queryset.exists():
            return Response("Already Present",
                            status=status.HTTP_208_ALREADY_REPORTED)
        serializer.save()


class CompetitionView(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnlyIfAuthenticated]
    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer

    def perform_create(self, serializer):
        queryset = Competition.objects.all()
        if queryset.exists():
            return Response("Already Present",
                            status=status.HTTP_208_ALREADY_REPORTED)
        serializer.save()


class EntryView(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnlyIfAuthenticated]
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer


class FormView(viewsets.ModelViewSet):
    permission_class = [IsAdminOrReadOnlyIfAuthenticated]
    query_set = Form.objects.all()
    serializer_class = FormSerializer

    def perform_create(self, serializer):
        queryset = Form.objects.all()
        if queryset.exists():
            return Response("Already Present",
                            status=status.HTTP_208_ALREADY_REPORTED)
        serializer.save()
