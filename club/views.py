
from rest_framework import viewsets
from .models import Club, Competition, Announcement
from .permissions import IsClubOwner
from .serializers import ClubSerializer, CompetitionSerializer, \
    AnnouncementsSerializer


class ClubView(viewsets.ModelViewSet):
    permission_classes = [IsClubOwner]
    queryset = Club.objects.all()
    serializer_class = ClubSerializer
    lookup_field = 'username'


class CompetitionView(viewsets.ModelViewSet):
    permission_classes = [IsClubOwner]
    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer


class AnnouncementsView(viewsets.ModelViewSet):
    permission_classes = [IsClubOwner]
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementsSerializer
