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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('autocomplete/', include('autocomplete.urls')),
    path('connect/', include('connect.urls')),
    path('rating/', include('rating.urls')),
    path('pathfinders/', include('ecell.urls')),
    path('club/', include('club.urls')),
    path('authenticate/', include('authenticate.urls')),
    path('form/', include('form.urls')),
]
