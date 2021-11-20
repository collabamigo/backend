from rest_framework import viewsets, generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny

from authenticate.authbackend import DummyAuthentication
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


class ClubAnnouncements(generics.ListAPIView):
    authentication_classes = [DummyAuthentication, TokenAuthentication]
    permission_classes = [AllowAny]
    serializer_class = AnnouncementsSerializer

    def get_queryset(self):
        club = self.kwargs['club']
        return Announcement.objects.filter(club__username=club)


class ClubCompetition(generics.ListAPIView):
    authentication_classes = [DummyAuthentication, TokenAuthentication]
    permission_classes = [AllowAny]
    serializer_class = CompetitionSerializer

    def get_queryset(self):
        club = self.kwargs['club']
        return Competition.objects.filter(club__username=club)
