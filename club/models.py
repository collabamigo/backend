from django.db import models
from connect.models import Profile


class Club(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    picture = models.CharField(max_length=100)  # url
    college = models.CharField(max_length=100, default="IIIT-D")
    join_date = models.DateField(auto_now_add=True)
    admins = models.ManyToManyField(to="auth.User", reated_name="clubs")
    instagram = models.URLField(max_length=100, blank=True)
    linkedin = models.URLField(max_length=100, blank=True)
    facebook = models.URLField(max_length=100, blank=True)
    discord = models.URLField(max_length=100, blank=True)
    other = models.URLField(max_length=100, blank=True)


class Competition(models.Model):
    id = models.AutoField(primary_key=True)
    club = models.ManyToManyField(Club,
                                  related_name="competitions")
    name = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=280, blank=True)
    disabled = models.BooleanField(default=False)
    # form_closing_time = DateTimeField
    # form_opening_time = DateTimeField
    # competition_time = DateTimeField
