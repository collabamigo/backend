from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.core.mail import send_mail
from backend.settings import EMAIL_HOST_USER


class Todo(models.Model):
    id = models.BigAutoField(primary_key=True, unique=True,
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
    First_Name = models.CharField(max_length=30)
    Last_Name = models.CharField(max_length=30, blank=True)
    Gender = models.CharField(max_length=1, blank=True, default='NA')
    Degree = models.CharField(max_length=1, blank=True)
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
            if i >= '0' and i <= '9':
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


class Skill(models.Model):

    id = models.CharField(primary_key=True, unique=True,
                          max_length=30, auto_created=False,
                          serialize=False, verbose_name='ID')
    Teacher_set = ArrayField(ArrayField(
        models.CharField(max_length=30, blank=True), size=2), size=5)


class Teacher(models.Model):
    id = models.OneToOneField(
        Profile, unique=True,
        on_delete=models.CASCADE,
        primary_key=True,
        max_length=6,
        auto_created=False,
        serialize=False,
        verbose_name='ID'
    )
    Skill_set = ArrayField(ArrayField(
        models.CharField(max_length=30, blank=True), size=2,
        blank=True,
        default=list,
        null=True),
        size=5, blank=True, default=list, null=True)

    Contact = models.BigIntegerField(blank=True)
