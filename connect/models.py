from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.db import models
from django import forms


class Todo(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    completed = models.BooleanField(default=False)

    def _str_(self):
        return self.title


class Profile(models.Model):
    # id = models.CharField(primary_key=True, unique=True,
    #                       max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    age = models.IntegerField(blank=True)
    gender = models.CharField(max_length=30, blank=True)
    education = ArrayField(
        models.CharField(max_length=30, blank=True), size=2)
    email = models.EmailField(
        max_length=75, editable=False)
    contact = models.BigIntegerField(blank=False)
    handle = models.CharField(max_length=500, blank=True)
    isvendor = models.BooleanField()


class Teacher(models.Model):

    id = models.CharField(primary_key=True, unique=True,
                          max_length=30)
    Skill_set = ArrayField(
        models.CharField(max_length=30, blank=True), size=20)


class Skill(models.Model):

    id = models.CharField(primary_key=True, unique=True,
                          max_length=30)
    Teacher_set = ArrayField(
        models.CharField(max_length=30, blank=True), size=20)
