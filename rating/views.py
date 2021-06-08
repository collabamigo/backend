
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from . import ratingHandler

from connect import logger, permissions as connect_perm


class Rating(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
        connect_perm.IsOwner,)

    def get(self, request):
        if request.user.is_staff:
            student_id = str(request.query_params['id'])
        else:
            student_id = str(request.user.profile.id)
        users = request.query_params.getlist('users[]')
        return Response(ratingHandler.return_ratings(student_id,
                                                     users))

    def post(self, request):
        if 'teacher' in request.data and 'vote' in request.data and \
                int(request.data['vote']) in [-1, 0, +1]:

            # Superuser can imitate and vote as another user even if the
            # user's connection isn't approved
            if request.user.is_staff:
                student_id = str(request.query_params['id'])
            else:
                student_id = str(request.user.profile.id)
            if request.data['teacher'] in logger.list_approvals(
                    student_id) or request.user.is_staff:
                ratingHandler.set_ratings(request.user.profile.id,
                                          request.data['teacher'],
                                          int(request.data['vote']))

                return Response()
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
