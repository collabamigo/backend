import os

from django.conf import settings
from django.core.files.base import ContentFile
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.utils import timezone
from rest_framework import viewsets, generics
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_403_FORBIDDEN
from rest_framework.views import APIView
from django.core.files.storage import default_storage

from authenticate.authentication import DummyAuthentication, CustomAuthentication
from authenticate.permissions import IsTrulyAuthenticated
from form.models import Form
from .models import Club, Competition, Announcement, CompetitionWinner
from .permissions import IsClubOwnerOrReadOnly, CompetitionWinnerPermission, IsClubOwner, IsClubMemberOrReadOnly
from .serializers import ClubSerializer, CompetitionSerializer, \
    AnnouncementsSerializer, CompetitionWinnerSerializer

from backend.settings import GOOGLE_SERVICE_ACCOUNT_CREDENTIALS
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload
from googleapiclient import discovery


class ClubViewSet(viewsets.ModelViewSet):
    permission_classes = [IsClubOwnerOrReadOnly]
    queryset = Club.objects.all()
    serializer_class = ClubSerializer
    lookup_field = 'username'


class CompetitionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsClubOwnerOrReadOnly | IsClubMemberOrReadOnly]
    queryset = Competition.objects.all().prefetch_related("clubs")
    serializer_class = CompetitionSerializer

    def perform_create(self, serializer):
        serializer.save(is_active=False)

    def perform_update(self, serializer):
        serializer.save(is_active=False)


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
        return Competition.objects.filter(clubs__username=club).prefetch_related("clubs")


class FeedView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):
        return JsonResponse(
            {
                'competitions': CompetitionSerializer(Competition.objects.filter(Q(is_active=True) &
                                                                                 Q(event_end__gt=timezone.now()) |
                                                                                 Q(event_end=None) &
                                                                                 Q(event_start__gt=timezone.now()) |
                                                                                 Q(form__closes_at__gt=timezone.now()),
                                                                                 ).order_by("-priority",
                                                                                            "event_start",
                                                                                            "form__closes_at",
                                                                                            "form__opens_at")[:10],
                                                      many=True).data,
                'clubs': ClubSerializer(Club.objects.filter(is_active=True), many=True).data,
            }
        )


class CompetitionWinnerViewSet(viewsets.ModelViewSet):
    permission_classes = [CompetitionWinnerPermission]
    serializer_class = CompetitionWinnerSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return CompetitionWinner.objects.all()
        else:
            return CompetitionWinner.objects.filter(competition__clubs__admins=user)


def handle_uploaded_file(f):
    # i think Google upload will come here
    # with open('some/file/name.txt', 'wb+') as destination:
    #     for chunk in f.chunks():
    #         destination.write(chunk)
    return True


@api_view(
    [
        "POST",
    ]
)
@permission_classes([IsClubOwnerOrReadOnly])
def upload_file(request):
    if request.method == 'POST':
        handle_uploaded_file(request.FILES['file'])
        return HttpResponseRedirect('/success/url/')


class EnableCompetitions(APIView):
    permission_classes = [IsTrulyAuthenticated]

    def post(self, request):
        competition_id, competition_state = int(request.data.get('competitionID')), \
                                            bool(int(request.data.get('is_active')))
        competition = Competition.objects.get(id=competition_id)
        organising_clubs = competition.clubs.all()

        club_coordinator_of = request.user.club_coordinator_of.all()
        if not (organising_clubs & club_coordinator_of).exists():
            return Response(status=HTTP_403_FORBIDDEN)

        competition.is_active = competition_state
        competition.save()

        return Response({
            'success': True
        })


class FileUpload(APIView):

    def post(self, request):
        file_uploaded = request.FILES.get('file_uploaded')
        form_no, form_field_no = int(request.data.get("form_no")), int(request.data.get("field_no"))
        form_for_competition = Form.objects.get(id=form_no)
        competition_name = form_for_competition.competition
        organising_club = competition_name.clubs.all()[:1].get()
        competition_name = competition_name.name
        handle_file_upload(file_uploaded, organising_club, form_no, form_field_no)

        return Response({
            "success": True
        })


def handle_file_upload(file, folder_name, form_no, form_field_no):
    credentials = credentials_from_file()

    # Construct a resource for interacting with API
    service = discovery.build('drive', 'v3', credentials=credentials)

    # Creating the media file upload object
    file_name = str(file.name)
    path = default_storage.save(os.path.join('tmp', file_name), ContentFile(file.read()))
    file.close()
    media = MediaFileUpload(os.path.join('tmp', file_name), mimetype=None)
    file.close()

    #Creating folder
    # First for Club

    check = 0
    response = service.files().list(
        q="mimeType='application/vnd.google-apps.folder'",
    ).execute()

    id_for_folder = 0
    for file in response.get('files', []):
        if str(file.get('name')) == str(folder_name):
            check += 1
            id_for_folder = file.get('id')
            break


    if(check == 0):
        file_metadata = {
            'name': str(folder_name),
            'parents': ['142JJ1d62qZc64qsf97M8W_KzuOIIvD9p'],
            'mimeType': 'application/vnd.google-apps.folder'
        }
        file = service.files().create(body=file_metadata,
                                      fields='id').execute()

        id_for_folder = file.get('id')

    print(id_for_folder)


    # Actual post : creating a new file of the uploaded type
    file_metadata = {
        'name': file_name,
        'parents': [str(id_for_folder)]
    }
    service.files().create(body=file_metadata, media_body=media).execute()

    os.remove(os.path.join(settings.MEDIA_ROOT, path))


def credentials_from_file():
    """Load credentials from a service account file
    Returns: service account credential object
    """

    SCOPES = [
        'https://www.googleapis.com/auth/drive'
    ]

    credentials = service_account.Credentials.from_service_account_info(GOOGLE_SERVICE_ACCOUNT_CREDENTIALS,
                                                                        scopes=SCOPES)

    return credentials
