from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from connect.permissions import IsAdminOrReadOnlyIfAuthenticated
from .models import Idea
from serializers import IdeaSerializer


# Create your views here.
class IdeaView(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnlyIfAuthenticated]
    queryset = Idea.objects.all()
    serializer_class = IdeaSerializer
    # lookup_field = 'username'

    def perform_create(self, serializer):
        queryset = Idea.objects.all()
        if queryset.exists():
            return Response("Already Present",
                            status=status.HTTP_208_ALREADY_REPORTED)
        serializer.save()
