from rest_framework import routers
from . import views
from backend import settings

if settings.DEVELOPMENT:
    router = routers.DefaultRouter()
else:
    router = routers.SimpleRouter()

router.register(r'user-device', views.UserDeviceViewSet, 'user_device_viewset')

urlpatterns = [
]

urlpatterns += router.urls
