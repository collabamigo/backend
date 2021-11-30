from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny

from authenticate.authbackend import DummyAuthentication, CustomAuthentication
from .models import Club, Competition, Announcement
from .permissions import IsClubOwnerOrReadOnly
from .serializers import ClubSerializer, CompetitionSerializer, \
    AnnouncementsSerializer


class ClubView(viewsets.ModelViewSet):
    permission_classes = [IsClubOwnerOrReadOnly]
    queryset = Club.objects.all()
    serializer_class = ClubSerializer
    lookup_field = 'username'


class CompetitionView(viewsets.ModelViewSet):
    permission_classes = [IsClubOwnerOrReadOnly]
    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer


class AnnouncementsView(viewsets.ModelViewSet):
    permission_classes = [IsClubOwnerOrReadOnly]
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementsSerializer


class ClubAnnouncements(generics.ListAPIView):
    authentication_classes = [DummyAuthentication, CustomAuthentication]
    permission_classes = [AllowAny]
    serializer_class = AnnouncementsSerializer

    def get_queryset(self):
        club = self.kwargs['club']
        return Announcement.objects.filter(club__username=club)


class ClubCompetition(generics.ListAPIView):
    authentication_classes = [DummyAuthentication, CustomAuthentication]
    permission_classes = [AllowAny]
    serializer_class = CompetitionSerializer

    def get_queryset(self):
        club = self.kwargs['club']
        return Competition.objects.filter(clubs__username=club)
