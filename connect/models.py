from django.contrib.postgres.fields import ArrayField
from django.db import models

from django.contrib.auth.models import User
User._meta.get_field('email')._unique = True

# from django.core.mail import send_mail
# from backend.settings import EMAIL_HOST_USER


class Todo(models.Model):
    id = models.CharField(primary_key=True, unique=True,
                          max_length=6,
                          auto_created=False,
                          serialize=False, verbose_name='ID')
    First_Name = models.CharField(max_length=30, blank=True)
    Last_Name = models.CharField(max_length=30, blank=True)
    Gender = models.CharField(max_length=10, blank=True, default='N')
    Degree = models.CharField(max_length=10, blank=True)
    Course = models.CharField(max_length=10, blank=True)
    Email = models.EmailField(max_length=50, unique=True, blank=False)
    Handle = models.CharField(max_length=50, blank=True)
    IsTeacher = models.BooleanField(default=False)

    def _str_(self):
        return self.Email

    def getrollnumber(self):
        x = str(self.Email)
        output = ""
        for i in x:
            if '0' <= i <= '9':
                output += i

        m = str(self.Degree) + output
        return m

    def save(self, *args, **kwargs):
        self.id = self.getrollnumber()
        super().save(*args, **kwargs)
        if self.IsTeacher:
            teach = Teacher()
            teach.id = self
            teach.save()
        # send_mail(
        #     'Registered',
        #     'You have been registered ' + self.id,
        #     EMAIL_HOST_USER,
        #     [self.Email],
        #     fail_silently=False,
        # )


class Profile(models.Model):
    id = models.CharField(primary_key=True, unique=True,
                          max_length=6,
                          auto_created=False,
                          serialize=False, verbose_name='ID')
    First_Name = models.CharField(max_length=30)
    Last_Name = models.CharField(max_length=30, blank=True)
    Gender = models.CharField(max_length=1, blank=True, )
    Degree = models.CharField(max_length=1, blank=True)
    Course = models.CharField(max_length=10, blank=True)
    Handle = models.CharField(max_length=50, blank=True)
    IsTeacher = models.BooleanField(default=False)
    Created = models.DateTimeField(auto_now_add=True)
    email = models.OneToOneField(to='auth.User',
                                 on_delete=models.CASCADE,
                                 related_name='profile',
                                 to_field='email',
                                 db_column='email')

    def _str_(self):
        return self.email

    def get_roll_number(self):
        x = str(self.email)
        output = ""
        for i in x:
            if '0' <= i <= '9':
                output += i

        m = str(self.Degree) + output
        return m

    def lol(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.id = self.get_roll_number()
        super().save(*args, **kwargs)
        # if self.IsTeacher:
        #     teach = Teacher()
        #     teach.id = self
        #     teach.save()
        # send_mail(
        #     'Registered',
        #     'You have been registered ' + self.id,
        #     EMAIL_HOST_USER,
        #     [self.Email],
        #     fail_silently=False,
        # )


class Skill(models.Model):
    id = models.CharField(primary_key=True, unique=True,
                          max_length=30, auto_created=False,
                          serialize=False, verbose_name='ID')
    Teacher_set = ArrayField(models.CharField
                             (max_length=30, blank=True))
# [[1,2],[2,3],[3,4],[5,6],[5,7]]
# [["hfgdfsddfgh","dfghj"]]


class Teacher(models.Model):
    id = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE,
        primary_key=True)

    Skill_set = ArrayField(ArrayField(
        models.CharField(max_length=100, blank=True), size=2,
        blank=True,
        default=list,
        null=True),
        size=5, blank=True, default=list, null=True)

    Contact = models.BigIntegerField(blank=True, default=0)
    UpVotes = models.BigIntegerField(blank=True, default=0)
    DownVotes = models.BigIntegerField(blank=True, default=0)

    # Email = models.OneToOneField(to='auth.User',
    #                              on_delete=models.CASCADE,
    #                              related_name='profile')

    def get_roll_number(self):
        x = str(self.id)
        output = ""
        for i in x:
            if i == 'B' or i == 'M':
                output += i
            if '0' <= i <= '9':
                output += i
        return output

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        print(self.id, flush=True)
        iid = self.get_roll_number()
        print(iid, type(iid), flush=True)
        b = Profile.objects.get(id=iid)
        b.IsTeacher = True
        b.lol()

    def delete(self, *args, **kwargs):
        iid = self.get_roll_number()
        b = Profile.objects.get(id=iid)
        b.IsTeacher = False
        b.lol()
        super().delete(*args, **kwargs)

    # if self.IsTeacher:
    #     teach = Teacher()
    #     teach.id = self
    #     teach.save()
    # send_mail(
    #     'Registered',
    #     'You have been registered ' + self.id,
    #     EMAIL_HOST_USER,
    #     [self.Email],
    #     fail_silently=False,
    # )
