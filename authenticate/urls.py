from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('oauthcallback/', views.OAuthCallback.as_view()),
    path('refresh/', views.RefreshJWT.as_view()),
    path('get-firebase-token/', views.GetFirebaseToken.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
