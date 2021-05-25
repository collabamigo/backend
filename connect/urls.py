from django.urls import path, include
from rest_framework import routers
from . import views
router = routers.DefaultRouter()

router.register(r'profile', views.ProfileView, 'profile')
router.register(r'teacher', views.TeacherView, 'teacher')
router.register(r'skill', views.SkillView, 'skill')

# TODO: #2 Better url names
urlpatterns = [
    path('teachersdata/', views.teachersdata, name='teachersdata'),
    path('api/', include(router.urls))]
