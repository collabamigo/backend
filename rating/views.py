import json

from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from connect.permissions import IsOwner
from . import ratingHandler


class Rating(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwner, )

    def get(self, request):
        users = request.GET
        if users:
            users = json.loads(users)
        return Response(ratingHandler.return_ratings(request.user.email,
                                                     users))

    def post(self, request):
        if 'teacher' in request.data and 'vote' in request.data and \
                int(request.data['vote']) in [-1, 0, +1]:
            ratingHandler.set_ratings(request.user.email,
                                      request.data['teacher'],
                                      int(request.data['vote']))
            return Response()
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
