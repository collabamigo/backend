from rest_framework import views, permissions, status
from rest_framework.response import Response

from . import TrieManager


class Recommendations(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if "query" in request.GET:
            return Response(
                TrieManager.get_recommendations(request.GET['query'],
                                                request.GET.get('cache')))
        else:
            # TODO: Remove worker function
            TrieManager.worker_generate_trie()
            return Response(
                "This is a bad request."
                "DO NOT ATTEMPT TO CALL THE API DIRECTLY."
                "ALSO, stop putting worker functions like that. It's lazy af",
                status=status.HTTP_400_BAD_REQUEST)
