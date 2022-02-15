from rest_framework import viewsets

from authenticate.permissions import IsTrulyAuthenticated
from .models import UserDevice
from .serializers import UserDeviceSerializer


class UserDeviceViewSet(viewsets.ModelViewSet):
    permission_classes = [IsTrulyAuthenticated]
    serializer_class = UserDeviceSerializer
    http_method_names = ['get', 'head', 'options', 'post']

    def get_queryset(self):
        if self.request.user.is_superuser:
            return UserDevice.objects.all()
        return UserDevice.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
