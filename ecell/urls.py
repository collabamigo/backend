from django.urls import path
from rest_framework import routers
from . import views
from backend import settings

if settings.DEVELOPMENT:
    router = routers.DefaultRouter()
else:
    router = routers.SimpleRouter()

router.register(r'club', views.IdeaView, 'club')

urlpatterns = [
    path('clubdata/', views.IdeaView, name='IdeaView'),
]

urlpatterns += router.urls
