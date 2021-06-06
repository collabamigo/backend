from django.urls import path
from rest_framework import routers
from . import views
from backend import settings

if settings.DEBUG:
    router = routers.DefaultRouter()
else:
    router = routers.SimpleRouter()

router.register(r'profile', views.ProfileView, 'profile')
router.register(r'teacher', views.TeacherView, 'teacher')
router.register(r'skill', views.SkillView, 'skill')

# TODO: #2 Better url names
urlpatterns = [
    path('teachersdata/', views.TeachersData.as_view(), name='TeachersData'),
    path('request/', views.ConnectionRequest.as_view(), name='request'),
    path('approve/', views.ConnectionApprove.as_view(), name='approve'),
    path('approvals/', views.ApprovalsView.as_view(), name='approvals'),

    path('statistics/skills', views.PopularSkills.as_view(),
         name='skill_stats')]

urlpatterns += router.urls
