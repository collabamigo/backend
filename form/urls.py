from django.urls import path, re_path
from rest_framework import routers
from . import views
from backend import settings

if settings.DEVELOPMENT:
    router = routers.DefaultRouter()
else:
    router = routers.SimpleRouter()

router.register(r'form', views.FormView, 'form')

urlpatterns = [
    path('submit/<int:event_id>/<str:submission_type>/', views.SubmitResponseView.as_view(), name='submit_response'),
    re_path('^response/(?P<competition_id>.+)/$', views.ResponseDisplayView.as_view(), name='response_display'),
    re_path('^get-response/(?P<competition_id>.+)/$', views.SelfFormResponseAPIView.as_view(),
            name='self_response_display'),
    path('participation-history/', views.ParticipationHistoryView.as_view(), name='participation_history'),
]

urlpatterns += router.urls
