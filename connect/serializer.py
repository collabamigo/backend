from rest_framework import serializers
from . models import *

class ReactSerializer(serializers.ModelSerializer):
	class Meta:
		model = React
		fields = ['_id', 'first_name','last_name','Age','Gender','Email','Contact','handle','isvendor']