from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render
from rest_framework import viewsets
from .serializer import *
from .models import *


# from django.http import HttpResponse
# from django.views.generic import View

# from django_mongoengine.forms.fields import DictField
# from django_mongoengine.views import (
#     CreateView, UpdateView,
#     DeleteView, ListView,
#     DetailView,
#     EmbeddedDetailView,
# )
# Create your views here.

class TodoView(viewsets.ModelViewSet):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()


# class ReactView(viewsets.ModelViewSet):

#     serializer_class = ReactSerializer
#     queryset = React.objects.all()

#     def get(self, request):
#         detail = [{'iid': detail._id, "first_name": detail.first_name, "first_name": detail.first_name, "Age": detail.Age, "Gender": detail.Gender, "Email": detail.Email, "Contact": detail.Contact, "handle": detail.handle, "isvendor": detail.isvendor}
#                   for detail in React.objects.all()]
#         return Response(detail)

#     def post(self, request):
#         print(request.data, " is request data")
#         serializer = ReactSerializer(data=request.data)
#         # trial = mySerializer(request.da)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             print(serializer.data, "is serialized data")
#             return Response(serializer.data)

# # class CredentialsView(View):

# # 	serializer_class = CredentialsSerializer
# # 	queryset = Credentials.objects.all()


# # class TeacherView(CreateView):

# # 	serializer_class = TeacherSerializer
# # 	queryset = Teacher.objects.all()
# # 	QuerySet = Teacher.objects.all()
# # e

# # class TestSessionView(View):


# # 	def get(self, request, *args, **kwargs):
# # 		test_data = request.session.get('test', None)
# # 		request.session['test'] = 'abc123'
# # 		return HttpResponse('test=%s' % test_data)
# # from tumblelog.models import Post, BlogPost, Video, Image, Quote, Music
# # from tumblelog import forms


# # class AddPostView(CreateView):
# #     doc_map = {'Skill_set': Teacher.Skill_set, 'helo': Teacher.helo}
# #     success_message = "Post Added!"
# #     fields = "__all__"

# #     @property
# #     def document(self):
# #         post_type = self.kwargs.get('post_type', 'post')
# #         return self.doc_map.get(post_type)

# #     def get_form(self, form_class=None):
# #         form = super(AddPostView, self).get_form(form_class)
# #         # music_parameters = form.fields.get('music_parameters', None)
# #         # if music_parameters is not None:
# #         # 	schema = {
# #         # 		'Artist': '',
# #         # 		'Title': '',
# #         # 		'Album': '',
# #         # 		'Genre': '',
# #         # 		'Label': '',
# #         # 		'Release dates': {
# #         # 			'UK': '',
# #         # 			'US': '',
# #         # 			'FR': ''
# #         # 		}
# #         # 	}
# #         # 	music_parameters = DictField(initial=schema, flags=['FORCE_SCHEMA'])
# #         # 	form.fields['music_parameters'] = music_parameters
# #         return form
