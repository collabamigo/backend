from django.db import models

from backend.settings import AUTH_USER_MODEL
from connect.models import Profile


class Idea(models.Model):
    id = models.AutoField(primary_key=True)
    # role = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    owners = models.ManyToManyField(Profile, related_name='ideas')
    estimate_time = models.DateField()
    team_size = models.IntegerField(blank=False, default=1)
    tags = models.TextField(blank=True)
    idea = models.TextField(max_length=900)
    visibility = models.BooleanField(default=False)
    stage = models.CharField(max_length=40, choices=[("i", "Initiation"),
                                                     ("p", "Planning"),
                                                     ("e", "Execution"),
                                                     ("mc", "Monitoring and"
                                                            " Controlling"),
                                                     ("c", "Closure")])
    college = models.CharField(max_length=100, default="IIIT-D")
    join_date = models.DateField(auto_now_add=True)
    bookmarked_by = models.ManyToManyField(Profile, related_name='bookmarked_ideas')


class ZeroToOneUser(models.Model):
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='zero_to_one_user')
    join_date = models.DateTimeField(auto_now_add=True)
    tnc_stage = models.IntegerField(default=0)
