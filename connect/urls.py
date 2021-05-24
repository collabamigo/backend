from django.urls import path, include
from rest_framework import routers
from . import views
router = routers.DefaultRouter()

router.register(r'todo', views.TodoView, 'todo')
router.register(r'profile', views.ProfileView, 'profile')
router.register(r'teacher', views.TeacherView, 'teacher')
router.register(r'skill', views.SkillView, 'skill')

# TODO: #2 Better url names
urlpatterns = [
    path('teacheridfor/<str:search>/', views.teacheridsfor,
         name='teacheridsfor'),
    path('teachersdata/', views.teachersdata, name='teachersdata'),
    path('get_profile/', views.Profilegetter, name='Profilegetter'),
    path('api/', include(router.urls)), ]
