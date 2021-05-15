from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework import generics, mixins
from .models import Todo, Profile, Teacher, Skill
from rest_framework import viewsets
from .serializer import (TodoSerializer, ProfileSerializer,
                         TeacherSerializer, SkillSerializer)
from rest_framework.parsers import JSONParser


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
        data['Email'] = request.email
        serializer = TodoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


def Profilegetter(request, Value):
    qm = (x for x in Profile.objects.filter(Email=Value)[::])
    output = ', '.join([q.id for q in qm])
    return JsonResponse(output, safe=False)


def detail(request, titlee):
    qm = (x for x in Todo.objects.filter(title=titlee)[::])
    output = ', '.join([q.description for q in qm])
    return JsonResponse(output, safe=False)


class CustomCreateModelMixin:
    """
    Create a model instance.
    """

    def create(self, request, *args, **kwargs):
        request.data["Email"] = request.email
        print(request, flush=True)
        # noinspection PyTypeChecker
        return mixins.CreateModelMixin.create(self,
                                              request,
                                              *args, **kwargs)

    perform_create = mixins.CreateModelMixin.perform_create
    get_success_headers = mixins.CreateModelMixin.perform_create


class GenericViewSet(viewsets.ViewSetMixin, generics.GenericAPIView):
    """
    The GenericViewSet class does not provide any actions by default,
    but does include the base set of generic view behavior, such as
    the `get_object` and `get_queryset` methods.
    """
    pass


@method_decorator(csrf_exempt, name='dispatch')
class TodoView(CustomCreateModelMixin,
               mixins.RetrieveModelMixin,
               mixins.UpdateModelMixin,
               mixins.DestroyModelMixin,
               mixins.ListModelMixin,
               GenericViewSet):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()


@method_decorator(csrf_exempt, name='dispatch')
class ProfileView(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()


@method_decorator(csrf_exempt, name='dispatch')
class TeacherView(viewsets.ModelViewSet):
    serializer_class = TeacherSerializer
    queryset = Teacher.objects.all()


@method_decorator(csrf_exempt, name='dispatch')
class SkillView(viewsets.ModelViewSet):
    serializer_class = SkillSerializer
    queryset = Skill.objects.all()
