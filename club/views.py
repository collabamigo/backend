# from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from connect.permissions import IsAdminOrReadOnlyIfAuthenticated
from .models import Club, Competition
from .serilaizers import ClubSerializer, CompetitionSerializer


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