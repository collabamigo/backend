from django.urls import path
from rest_framework import routers
from . import views
from backend import settings

if settings.DEBUG:
    router = routers.DefaultRouter()
else:
    router = routers.SimpleRouter()

router.register(r'club', views.ClubView, 'club')

urlpatterns = [
    path('clubdata/', views.ClubView, name='ClubData'),
]

urlpatterns += router.urls
