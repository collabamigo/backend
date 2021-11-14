
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Club, Competition, Announcement
from .permissions import IsClubOwner
from .serializers import ClubSerializer, CompetitionSerializer, \
    AnnouncementsSerializer


# Create your views here.

class ClubView(viewsets.ModelViewSet):
    permission_classes = [IsClubOwner]
    queryset = Club.objects.all()
    serializer_class = ClubSerializer
    lookup_field = 'username'

    def perform_create(self, serializer):
        queryset = Club.objects.all()
        if queryset.exists():
            return Response("Already Present",
                            status=status.HTTP_208_ALREADY_REPORTED)
        serializer.save()


class CompetitionView(viewsets.ModelViewSet):
    permission_classes = [IsClubOwner]
    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer

    def perform_create(self, serializer):
        queryset = Competition.objects.all()
        if queryset.exists():
            return Response("Already Present",
                            status=status.HTTP_208_ALREADY_REPORTED)
        serializer.save()


class AnnouncementsView(viewsets.ModelViewSet):
    permission_classes = [IsClubOwner]
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementsSerializer

    def perform_create(self, serializer):
        queryset = Announcement.objects.all()
        if queryset.exists():
            return Response("Already Present",
                            status=status.HTTP_208_ALREADY_REPORTED)
        serializer.save()
