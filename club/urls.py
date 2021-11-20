from django.urls import path, re_path
from rest_framework import routers
from . import views
from backend import settings

if settings.DEVELOPMENT:
    router = routers.DefaultRouter()
else:
    router = routers.SimpleRouter()

router.register(r'club', views.ClubView, 'club')
router.register(r'competition', views.CompetitionView, 'Competition')
router.register(r'announcements', views.AnnouncementsView, 'Announcements')

urlpatterns = [
    re_path('^clubannouncements/(?P<club>.+)/$', views.ClubAnnouncements.as_view()),
    re_path('^clubcompetitions/(?P<club>.+)/$', views.ClubCompetition.as_view()),
]

urlpatterns += router.urls
