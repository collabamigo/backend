from django.db import models


# Create your models here.
class Ecell(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, default='null')
    role = models.CharField(max_length=8, choices=["ideator", "member"])
    batch = models.IntegerField(default="null")
    stream = models.CharField(default="null")
    email = models.EmailField(default="null@gmail.com")
    mobile_number = models.BigIntegerField(default="null")
    idea = models.TextField(max_length=900)
    visibility = models.CharField(max_length=8, choices=["public", "private"])
    stage = models.CharField(max_length=40, choices=["Initiation", "Planning",
                                                     "Execution",
                                                     "Monitoring and"
                                                     " Controllling",
                                                     "Closure"])
    college = models.CharField(max_length=100, default="IIIT-D")
    join_date = models.DateField(auto_now_add=True)
