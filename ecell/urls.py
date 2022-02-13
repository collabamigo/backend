from django.urls import path
from rest_framework import routers
from . import views
from backend import settings

if settings.DEVELOPMENT:
    router = routers.DefaultRouter()
else:
    router = routers.SimpleRouter()

router.register(r'all', views.IdeaView, 'ecell')

urlpatterns = [
    path('mine/', views.SelfIdeaAPIView.as_view(), name='self_idea'),
    path('bookmarks/', views.BookmarkAPIView.as_view(), name='bookmark'),
    path('tnc/', views.TnCStageAPIView.as_view(), name='tnc'),
]

urlpatterns += router.urls
