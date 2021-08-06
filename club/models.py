from django.db import models
from connect.models import Profile


# Create your models here.
class Club(models.Model):
    id = models.CharField(primary_key=True, unique=True,
                          max_length=6, auto_created=False,
                          serialize=False, verbose_name='ID')
    name = models.CharField(max_length=50)
    link = models.CharField(max_length=100)  # url
    picture = models.CharField(max_length=100)  # url
    college = models.CharField(default="IIIT-D")
    join_date = models.DateField()


class Competition(models.Model):
    competition_id = models.IntegerField(primary_key=True, unique=True,
                                         max_length=6, auto_created=False,
                                         serialize=False, verbose_name='ID')
    on_going = models.BooleanField()
    # competitions = models.ManyToManyField(related_name='Club', on_delete=models.CASCADE)


class Entries(models.Model):
    entries_id = models.ForeignKey(Competition.competition_id, on_delete=models.CASCADE)
    participant = models.ForeignKey(Profile, on_delete=models.CASCADE)


class Form(models.Model):
    id = models.IntegerField(primary_key=True, unique=True,
                             max_length=6, auto_created=False,
                             serialize=False, verbose_name='ID')
