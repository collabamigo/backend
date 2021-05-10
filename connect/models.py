from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.core.mail import send_mail
from backend.settings import EMAIL_HOST_USER


class Todo(models.Model):
    id = models.AutoField(primary_key=True, unique=True,
                          auto_created=True,
                          serialize=False, verbose_name='ID')
    title = models.CharField(max_length=120)
    description = models.TextField()
    completed = models.BooleanField(default=False)

    def _str_(self):
        return self.title


class Profile(models.Model):
    id = models.CharField(primary_key=True, unique=True,
                          max_length=6,
                          auto_created=False,
                          serialize=False, verbose_name='ID')
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    age = models.IntegerField(blank=True)
    gender = models.CharField(max_length=1, blank=True)
    education = ArrayField(
        models.CharField(max_length=5, blank=True), size=2)
    email = models.EmailField(max_length=50, unique=True)
    contact = models.BigIntegerField(blank=False, unique=True)
    handle = models.CharField(max_length=50, blank=True)
    isteacher = models.BooleanField(default=False)

    def _str_(self):
        return self.email

    def getrollnumber(self):
        x = str(self.email)
        print(x)
        print(self.id)
        output = ""
        for i in x:
            if i >= '0' and i <= '9':
                output += i

        m = str(self.education[0])[0] + output
        return m

    def teacher(self):
        obj = Teacher()
        obj.id = self.id
        obj.related = self.id
        obj.save()

    def save(self, *args, **kwargs):
        self.id = self.getrollnumber()
        send_mail(
            'Registered',
            'You have been registered',
            EMAIL_HOST_USER,
            [self.email],
            fail_silently=False,
        )

        if isteacher:
            self.teacher()
        super().save(*args, **kwargs)  # Call the "real" save() method.


class Teacher(models.Model):

    id = models.CharField(primary_key=True, unique=True,
                          max_length=30, auto_created=False,
                          serialize=False, verbose_name='ID')
    Skill_set = ArrayField(ArrayField(
        models.CharField(max_length=30, blank=True), size=2), size=5)
    related = models.ForeignKey('Profile', on_delete=models.CASCADE)


class Skill(models.Model):

    id = models.CharField(primary_key=True, unique=True,
                          max_length=30, auto_created=False,
                          serialize=False, verbose_name='ID')
    Teacher_set = ArrayField(ArrayField(
        models.CharField(max_length=30, blank=True), size=2), size=5)
