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

# STYLE_CHOICES = [['I','Instagram'],['T','Telegram'],['S','Signal'],['Snap','Snapchat']]

# class Credentials(Document):
# 	_id= me.StringField(primary_key=True, max_length=30)
# 	first_name = me.StringField(max_length=30)
# 	last_name = me.StringField(max_length=30)
# 	Age = me.IntField()
# 	Gender = me.StringField(max_length=30)
# 	Education = me.DictField()
# 	Email = me.EmailField(max_length=75)
# 	Contact = me.LongField()
# 	handle = me.StringField(choices=STYLE_CHOICES, default='Telegram', max_length=100)
# 	handle_username = me.StringField(max_length=30,default="LOL")
# 	isvendor = me.BooleanField()



class Post(Document):
	    created_at = me.DateTimeField(
	        default=datetime.datetime.now, editable=False,
	    )
	    @property
	    def post_type(self):
	        return self.__class__.__name__
	
	    meta = {
	        'indexes': ['-created_at'],
	        'ordering': ['-created_at'],
	        'allow_inheritance': True
	    }

class Teacher(Post):
	
	Skill_set = me.ListField(me.StringField(max_length=30))
	helo = me.StringField(max_length=30)

