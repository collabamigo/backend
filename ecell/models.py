from django.db import models

from backend.settings import AUTH_USER_MODEL
from connect.models import Profile


class Idea(models.Model):
    id = models.AutoField(primary_key=True)
    # role = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    owners = models.ManyToManyField(Profile, related_name='ideas')
    duration = models.CharField(max_length=50, blank=True)
    team_size = models.IntegerField(blank=False, default=1)
    tags = models.TextField(blank=True)
    description = models.TextField(blank=True)
    updates = models.TextField(blank=True)
    onboarding = models.BooleanField(default=False)
    hidden = models.BooleanField(default=True)
    stage = models.CharField(max_length=40, blank=True)
    startedOn = models.DateField(auto_now_add=True)
    bookmarked_by = models.ManyToManyField(Profile, related_name='bookmarked_ideas', blank=True)
    form_filling_stage = models.IntegerField(default=0)
    social_links = models.TextField(blank=True)
    other = models.TextField(blank=True)
    contact_email = models.EmailField(blank=True)


class ZeroToOneUser(models.Model):
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='zero_to_one_user')
    join_date = models.DateTimeField(auto_now_add=True)
    tnc_stage = models.IntegerField(default=0)
