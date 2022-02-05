from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED
from rest_framework.views import APIView

from authenticate.permissions import IsTrulyAuthenticated
from connect.permissions import IsAdminOrReadOnlyIfAuthenticated
from .models import Idea, ZeroToOneUser
from .serializers import IdeaSerializer


class IdeaView(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnlyIfAuthenticated]
    serializer_class = IdeaSerializer
    # http_method_names = ['get', 'put', 'patch', 'delete']

    def get_queryset(self):
        return Idea.objects.filter(visibility=True)


class SelfIdeaAPIView(APIView):
    permission_classes = [IsTrulyAuthenticated]

    def get(self, request):
        ideas = Idea.objects.filter(owners=request.user.profile)
        serializer = IdeaSerializer(ideas, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        data['owners'] = [request.user.profile.id]
        serializer = IdeaSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def patch(self, request):
        data = request.data
        idea: Idea = Idea.objects.get(id=data['id'])
        if "owners" in data:
            del data['owners']
        if idea.owners.filter(id=request.user.profile.id).exists():
            serializer = IdeaSerializer(idea, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        return Response(status=HTTP_400_BAD_REQUEST)


class BookmarkAPIView(APIView):
    permission_classes = [IsTrulyAuthenticated]

    def get(self, request, *args, **kwargs):
        projects = request.user.bookmarked_ideas.all()
        serializer = IdeaSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        pk = request.data.get('pk')
        state = request.data.get('state')
        idea = Idea.objects.get(pk=pk)
        if state == "1":
            if idea not in request.user.bookmarked_ideas.all():
                request.user.bookmarked_ideas.add(idea)
                return Response({"message": "Bookmarked"}, status=HTTP_201_CREATED)
            else:
                return Response({"error": "Already bookmarked"}, status=HTTP_400_BAD_REQUEST)
        elif state == "0":
            if idea in request.user.bookmarked_ideas.all():
                request.user.bookmarked_ideas.remove(idea)
                return Response({"message": "Removed from bookmarks"}, status=HTTP_201_CREATED)
            else:
                return Response({"error": "Not bookmarked"}, status=HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Invalid state"}, status=HTTP_400_BAD_REQUEST)


class TnCStageAPIView(APIView):
    permission_classes = [IsTrulyAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response({"tnc_stage": request.user.zero_to_one_user.tnc_stage})

    def post(self, request, *args, **kwargs):
        tnc_stage = int(request.data.get('tnc_stage'))
        try:
            zero_to_one_user = ZeroToOneUser.objects.get(user=request.user)
        except ZeroToOneUser.DoesNotExist:
            zero_to_one_user = ZeroToOneUser(user=request.user)
        zero_to_one_user.tnc_stage = tnc_stage
        zero_to_one_user.save()
        return Response({"tnc_stage": tnc_stage})
