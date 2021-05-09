from rest_framework import routers
from . import views

router = routers.DefaultRouter()

router.register(r'todo', views.TodoView, 'todo')
router.register(r'profile', views.ProfileView, 'profile')
router.register(r'teacher', views.TeacherView, 'teacher')
router.register(r'skill', views.SkillView, 'skill')


urlpatterns = [
    path('<str:titlee>/', views.detail, name='detail'),
    path('api/', include(router.urls))]
