from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework import generics, permissions
from django.contrib.auth.models import User

from .models import Todo, Profile, Teacher, Skill
from rest_framework import viewsets

from .permissions import IsOwner
from .serializers import (TodoSerializer, ProfileSerializer,
                          TeacherSerializer, SkillSerializer, UserSerializer)
from rest_framework.parsers import JSONParser


@csrf_exempt
def Profilegetter(request):
    qm = (x for x in Profile.objects.get(Email=request.user.email))
    output = ', '.join([q for q in qm])
    return JsonResponse(output, safe=False)


@csrf_exempt
def profile_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Todo.objects.all()
        serializer = TodoSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        data['Email'] = request.user.email
        serializer = TodoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


# def Profilegetter(request, Value):
#     qm = (x for x in Profile.objects.filter(Email=Value)[::])
#     output = ', '.join([q.id for q in qm])
#     return JsonResponse(output, safe=False)


# def detail(request, titlee):
#     qm = (x for x in Todo.objects.filter(title=titlee)[::])
#     output = ', '.join([q.description for q in qm])
#     return JsonResponse(output, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class TodoView(viewsets.ModelViewSet):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()


@method_decorator(csrf_exempt, name='dispatch')
class ProfileView(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwner, )

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user = self.request.user
        if user.is_superuser:
            return Profile.objects.all()
        else:
            return Profile.objects.filter(Email=user)

    def perform_create(self, serializer):
        serializer.save(Email=self.request.user)


@method_decorator(csrf_exempt, name='dispatch')
class TeacherView(viewsets.ModelViewSet):
    serializer_class = TeacherSerializer
    queryset = Teacher.objects.all()


@method_decorator(csrf_exempt, name='dispatch')
class SkillView(viewsets.ModelViewSet):
    serializer_class = SkillSerializer
    queryset = Skill.objects.all()


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
