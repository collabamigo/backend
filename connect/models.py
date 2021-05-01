from django.db import models

class React(models.Model):
	_id= models.CharField(primary_key=True, max_length=30)
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)
	Age = models.IntegerField()
	Gender = models.CharField(max_length=30)
	# Education = serializers.DictField(child = serializers.CharField())
	Email = models.EmailField(max_length=75)
	Contact = models.BigIntegerField()
	handle = models.CharField(max_length=500)
	isvendor = models.BooleanField()