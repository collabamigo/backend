from rest_framework import viewsets
from connect.permissions import IsAdminOrReadOnlyIfAuthenticated
from .models import Idea
from .serializers import IdeaSerializer


class IdeaView(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnlyIfAuthenticated]
    queryset = Idea.objects.all()
    serializer_class = IdeaSerializer


class SelfIdeaView(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnlyIfAuthenticated]
    queryset = Idea.objects.all()
    serializer_class = IdeaSerializer

    def get_queryset(self):
        return Idea.objects.filter(owners__email=self.request.user)
