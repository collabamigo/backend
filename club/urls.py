from django.urls import path
from rest_framework import routers
from . import views
from backend import settings

if settings.DEBUG:
    router = routers.DefaultRouter()
else:
    router = routers.SimpleRouter()

router.register(r'club', views.ClubView, 'club')
router.register(r'competition', views.CompetitionView, 'Competition')
router.register(r'entry', views.EntryView, 'entry')

urlpatterns = [
    path('clubdata/', views.ClubView, name='ClubData'),
]

urlpatterns += router.urls
