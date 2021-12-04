# from django.urls import path
from django.urls import path
from rest_framework import routers
from . import views
from backend import settings

if settings.DEVELOPMENT:
    router = routers.DefaultRouter()
else:
    router = routers.SimpleRouter()

router.register(r'form', views.FormView, 'form')

urlpatterns = [
    path('submit/<int:event_id>/', views.SubmitResponseView.as_view(), name='submit_response'),
]

urlpatterns += router.urls
