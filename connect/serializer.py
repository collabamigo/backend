# from rest_framework import serializers
from mongoengine import *
from rest_framework_mongoengine import serializers
from rest_framework_mongoengine.serializers import *
from . models import *

# class ReactSerializer(serializers.ModelSerializer):
# 	class Meta:
# 		model = React
# 		fields = ['_id', 'first_name','last_name','Age','Gender','Email','Contact','handle','isvendor']

class CredentialsSerializer(DocumentSerializer):
	class Meta:
		abstract = False
		model = Credentials
		fields = ['_id','first_name','last_name','Age','Gender'
		,'Education','Email','Contact','handle',
		'handle_username','isvendor']


class TeacherSerializer(DocumentSerializer):
	class Meta:
		abstract = True
		model = Teacher
		fields = ['_id','Skill_set']