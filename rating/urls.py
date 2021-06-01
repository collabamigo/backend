from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('', views.Rating.as_view(), name='rating')
]

urlpatterns = format_suffix_patterns(urlpatterns)
