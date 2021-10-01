from django.urls import path
from rest_framework import routers
from . import views
from backend import settings

if settings.DEVELOPMENT:
    router = routers.DefaultRouter()
else:
    router = routers.SimpleRouter()

router.register(r'form','form')

urlpatterns = [
    path('form', views.FormView, name='form'),
]

urlpatterns += router.urls
