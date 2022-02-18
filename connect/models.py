from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth import get_user_model
from backend import settings

User = get_user_model()

# TODO: Synchronization of Naming conventions


class Profile(models.Model):
    id = models.CharField(primary_key=True, unique=True,
                          max_length=32, editable=True)
    First_Name = models.CharField(max_length=30)
    Last_Name = models.CharField(max_length=50, blank=True)
    gender = models.CharField(max_length=1, blank=True, )
    degree = models.CharField(max_length=1, blank=True)
    course = models.CharField(max_length=10, blank=True)
    handle = models.CharField(max_length=50, blank=True)
    email = models.OneToOneField(to=settings.AUTH_USER_MODEL,
                                 on_delete=models.CASCADE,
                                 related_name='profile',
                                 to_field='email')

    def __str__(self):
        return self.id


class Teacher(models.Model):
    id = models.OneToOneField(to=Profile, related_name='teacher',
                              to_field='id', db_column='id',
                              on_delete=models.CASCADE,
                              primary_key=True)
    Contact = models.BigIntegerField(blank=True, default=0,
                                     validators=[MinValueValidator(0)])
    UpVotes = models.BigIntegerField(blank=True, default=0,
                                     validators=[MinValueValidator(0)])
    DownVotes = models.BigIntegerField(blank=True, default=0,
                                       validators=[MinValueValidator(0)])
    confidence = models.FloatField(blank=True, default=0)
    Gitname = models.CharField(max_length=100, blank=True)
    Linkedin = models.CharField(max_length=100, blank=True)
    email = models.OneToOneField(to=settings.AUTH_USER_MODEL,
                                 on_delete=models.CASCADE,
                                 related_name='teacher',
                                 to_field='email')
    Created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = [
            '-confidence',
            '-UpVotes',
            'DownVotes', ]


class Skill(models.Model):
    name = models.CharField(primary_key=True, unique=True,
                            max_length=30, auto_created=False,
                            serialize=False, verbose_name='ID')
    Teacher_set = models.ManyToManyField(to='connect.Teacher',
                                         related_name='skills',
                                         blank=True, through='SkillSet')

    def __str__(self):
        return self.name


class SkillSet(models.Model):
    id = models.AutoField(primary_key=True)
    teacher = models.ForeignKey(Teacher,
                                on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill,
                              on_delete=models.CASCADE)
    approvals = models.IntegerField(blank=False, default=0)
