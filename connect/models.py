# from django.db import models
from mongoengine import fields as me
from mongoengine.document import Document
# class React(models.Model):
# 	_id= models.fields.StringField(primary_key=True, max_length=30)
# 	first_name = models.CharField(max_length=30)
# 	last_name = models.CharField(max_length=30)
# 	Age = models.IntegerField()
# 	Gender = me.StringField(max_length=30)
# 	# Education = serializers.DictField(child = serializers.CharField())
# 	Email = me.EmailField(max_length=75)
# 	Contact = models.BigIntegerField()
# 	handle = me.StringField(max_length=500)
# 	isvendor = me.BooleanField()

STYLE_CHOICES = [['I','Instagram'],['T','Telegram'],['S','Signal'],['Snap','Snapchat']]

class Credentials(Document):
	_id= me.StringField(primary_key=True, max_length=30)
	first_name = me.StringField(max_length=30)
	last_name = me.StringField(max_length=30)
	Age = me.IntField()
	Gender = me.StringField(max_length=30)
	Education = me.DictField(db_field=me.StringField(max_length=30))
	Email = me.EmailField(max_length=75)
	Contact = me.LongField()
	handle = me.StringField(choices=STYLE_CHOICES, default='Telegram', max_length=100)
	handle_username = me.StringField(max_length=30,default="LOL")
	isvendor = me.BooleanField()

class Teacher(Document):
	_id= me.StringField(primary_key=True, max_length=30)
	Skill_set = me.DictField(db_field=me.StringField(max_length=30))

