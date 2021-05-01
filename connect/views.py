from django.shortcuts import render
# from rest_framework.views import APIView
# from . models import *
# from rest_framework.response import Response
from rest_framework import viewsets
from .serializer import ReactSerializer
from .models import React
# Create your views here.

class ReactView(viewsets.ModelViewSet):
	
	serializer_class = ReactSerializer
	queryset = React.objects.all()

	def get(self, request):
		detail = [ {'_id': detail._id,"first_name": detail.first_name,"first_name": detail.first_name,"Age":detail.Age,"Gender":detail.Gender,"Email":detail.Email,"Contact":detail.Contact,"handle":detail.handle,"isvendor":detail.isvendor}
		for detail in React.objects.all()]
		return Response(detail)

	def post(self, request):
		print(request.data," is request data")
		serializer = ReactSerializer(data=request.data)
		# trial = mySerializer(request.da)
		if serializer.is_valid(raise_exception=True):
			serializer.save()
			print(serializer.data,"is serialized data")
			return  Response(serializer.data)