from django.contrib.postgres.fields import ArrayField
from django.db import models
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
    Gender = models.CharField(max_length=1, blank=True,)
    Degree = models.CharField(max_length=1, blank=True)
    Course = models.CharField(max_length=10, blank=True)
    Handle = models.CharField(max_length=50, blank=True)
    IsTeacher = models.BooleanField(default=False)
    Created = models.DateTimeField(auto_now_add=True)
    Email = models.ForeignKey('auth.User',
                              on_delete=models.CASCADE,
                              related_name='profile')

    def _str_(self):
        return self.Email

    def get_roll_number(self):
        x = str(self.Email)
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
    Teacher_set = ArrayField(ArrayField(
        models.CharField(max_length=30, blank=True), size=2), size=5)


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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        b = Profile.objects.get(id='B20064')
        b.IsTeacher = True
        b.lol()

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
