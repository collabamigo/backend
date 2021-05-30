from django.urls import path
from . import views

urlpatterns = [
    path('', views.Recommendations.as_view(), name='recommendations')
]
