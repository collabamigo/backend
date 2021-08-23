# from django.shortcuts import render
from rest_framework import viewsets

from connect.permissions import IsAdminOrReadOnlyIfAuthenticated
from .models import Club, Competition
from .serilaizers import ClubSerializer, CompetitionSerializer


# Create your views here.

class ClubView(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnlyIfAuthenticated]
    queryset = Club.objects.all()
    serializer_class = ClubSerializer


class CompetitionView(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnlyIfAuthenticated]
    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer
