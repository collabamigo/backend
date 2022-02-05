from django.urls import re_path, path
from rest_framework import routers
from . import views
from backend import settings

if settings.DEVELOPMENT:
    router = routers.DefaultRouter()
else:
    router = routers.SimpleRouter()

router.register(r'club', views.ClubViewSet, 'club')
router.register(r'competition', views.CompetitionViewSet, 'Competition')
router.register(r'announcements', views.AnnouncementsViewSet, 'Announcements')
router.register(r'competition-winner', views.CompetitionWinnerViewSet, 'CompetitionWinners')

urlpatterns = [
    re_path('^clubannouncements/(?P<club>.+)/$', views.ClubAnnouncements.as_view()),
    re_path('^clubcompetitions/(?P<club>.+)/$', views.ClubCompetition.as_view()),
    re_path('^feed/', views.FeedView.as_view()),
    path('upload-file/', views.upload_file, name='upload-file'),
]

urlpatterns += router.urls
