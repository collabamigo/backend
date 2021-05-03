from rest_framework import serializers
from . models import *

# class ReactSerializer(serializers.ModelSerializer):
# 	class Meta:
# 		model = React
# 		fields = ['_id', 'first_name','last_name','Age','Gender','Email','Contact','handle','isvendor']

class CredentialsSerializer(serializers.ModelSerializer):
	class Meta:
		abstract = False
		model = Credentials
		fields = ['_id','first_name','last_name','Age','Gender'
		,'Education','Email','Contact','handle',
		'handle_username','isvendor']


class TeacherSerializer(serializers.ModelSerializer):
	class Meta:
		abstract = False
		model = Teacher
		fields = ['_id','Skill_set']