from rest_framework import serializers
# from mongoengine import *
# from rest_framework_mongoengine import serializers
# from rest_framework_mongoengine.serializers import *
from . models import *


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('id', 'title', 'description', 'completed')


# class ReactSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = React
#         fields = ['iid', 'first_name', 'last_name', 'Age',
#                   'Gender', 'Email', 'Contact', 'handle', 'isvendor']

# class CredentialsSerializer(DocumentSerializer):
# 	class Meta:
# 		abstract = False
# 		model = Credentials
# 		fields = ['_id','first_name','last_name','Age','Gender'
# 		,'Education','Email','Contact','handle',
# 		'handle_username','isvendor']


# class TeacherSerializer(DocumentSerializer):
# 	class Meta:
# 		abstract = True
# 		model = Teacher
# 		fields = ['Skill_set','helo']
