from django.http import JsonResponse
from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.utils import timezone
from django.db.models import Q
from authenticate.authentication import DummyAuthentication, CustomAuthentication
from .models import Club, Competition, Announcement, CompetitionWinner
from .permissions import IsClubOwnerOrReadOnly, CompetitionWinnerPermission, IsClubOwner
from .serializers import ClubSerializer, CompetitionSerializer, \
    AnnouncementsSerializer, CompetitionWinnerSerializer


class ClubViewSet(viewsets.ModelViewSet):
    permission_classes = [IsClubOwnerOrReadOnly]
    queryset = Club.objects.all()
    serializer_class = ClubSerializer
    lookup_field = 'username'


class CompetitionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsClubOwnerOrReadOnly]
    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer

# TODO: Any club can add any other club's announcement


class AnnouncementsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsClubOwner]
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
    authentication_classes = []
    permission_classes = [AllowAny]
    serializer_class = CompetitionSerializer

    def get_queryset(self):
        club = self.kwargs['club']
        return Competition.objects.filter(clubs__username=club)


class FeedView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):
        return JsonResponse(
            {
                'competitions': CompetitionSerializer(Competition.objects.filter(Q(event_end__gt=timezone.now()) |
                                                                                 Q(event_end=None) &
                                                                                 Q(event_start__gt=timezone.now())
                                                                                 ).order_by("event_start")[:10],
                                                      many=True).data,
                'clubs': ClubSerializer(Club.objects.all(), many=True).data,
            }
        )


class CompetitionWinnerViewSet(viewsets.ModelViewSet):
    permission_classes = [CompetitionWinnerPermission]
    serializer_class = CompetitionWinnerSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return CompetitionWinner.objects.all()
        else:
            return CompetitionWinner.objects.filter(competition__clubs__admins=user)

