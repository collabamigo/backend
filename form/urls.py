# from django.urls import path
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
    path('submit/<int:event_id>/', views.SubmitResponseView.as_view(), name='submit_response'),
    re_path('^response/(?P<competition_id>.+)/$', views.ResponseDisplayView.as_view(), name='response_display'),
]

urlpatterns += router.urls
