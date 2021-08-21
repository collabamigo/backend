# from django.shortcuts import render
from rest_framework import viewsets
from .models import Club
from .serilaizers import ClubSerializer


# Create your views here.

class ClubView(viewsets.ModelViewSet):
    queryset = Club.objects.all()
    serializer_class = ClubSerializer
