from django.db import models


# Create your models here.
class Idea(models.Model):
    id = models.AutoField(primary_key=True)
    role = models.CharField(max_length=8, choices=[("i", "ideator"),
                                                   ("m", "member")])
    name = models.CharField(max_length=50, default='null')
    profile = models.OneToOneField(to="Profile", on_delete=models.CASCADE,
                                   related_name='profile')
    idea = models.TextField(max_length=900)
    visibility = models.CharField(max_length=8, choices=["public", "private"])
    stage = models.CharField(max_length=40, choices=[("i", "Initiation"),
                                                     ("p", "Planning"),
                                                     ("e", "Execution"),
                                                     ("mc", "Monitoring and"
                                                     " Controllling"),
                                                     ("c", "Closure")])
    college = models.CharField(max_length=100, default="IIIT-D")
    join_date = models.DateField(auto_now_add=True)
