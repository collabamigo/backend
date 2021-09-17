from django.urls import path
from rest_framework import routers
from . import views
from backend import settings

if settings.DEVELOPMENT:
    router = routers.DefaultRouter()
else:
    router = routers.SimpleRouter()

router.register(r'club', views.ClubView, 'club')
router.register(r'competition', views.CompetitionView, 'Competition')
router.register(r'entry', views.EntryView, 'entry')
router.register(r'formCreate', views.FormView, 'Form')

urlpatterns = [
    path('clubdata/', views.ClubView, name='ClubData'),
]

urlpatterns += router.urls
