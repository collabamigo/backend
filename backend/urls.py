"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from django.contrib import admin
from django.conf.urls import url
from connect.views import *
from rest_framework import routers
from connect import views
router = routers.DefaultRouter()
router.register(r'connect', views.TodoView, 'connect')

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('wel/', ReactView.as_view(), name="something"),
    path('api/', include(router.urls))]
# path('',home,name='home'),
# path('wel/', CredView.as_view(), name="something"),
# ]
