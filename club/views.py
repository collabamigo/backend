# from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Club
from .serilaizers import ClubSerializer


# Create your views here.

class ClubView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    queryset = Club.objects.all()
    serializer_class = ClubSerializer
