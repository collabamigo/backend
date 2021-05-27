# from connect.emailhandler import new_teacher_email
from django.db import models
from django.contrib.auth.models import User
User._meta.get_field('email')._unique = True


class Profile(models.Model):
    id = models.CharField(primary_key=True, unique=True,
                          max_length=6,
                          auto_created=False,
                          serialize=False, verbose_name='ID')
    First_Name = models.CharField(max_length=30)
    Last_Name = models.CharField(max_length=30, blank=True)
    gender = models.CharField(max_length=1, blank=True, )
    degree = models.CharField(max_length=1, blank=True)
    course = models.CharField(max_length=10, blank=True)
    handle = models.CharField(max_length=50, blank=True)
    IsTeacher = models.BooleanField(default=False)
    Created = models.DateTimeField(auto_now_add=True)
    email = models.OneToOneField(to='auth.User',
                                 on_delete=models.CASCADE,
                                 related_name='profile',
                                 to_field='email',
                                 db_column='email')

    def __str__(self):
        return self.id

# TODO: #3 Better ID extraction
    def get_roll_number(self):
        x = str(self.email)
        output = ""
        for i in x:
            if '0' <= i <= '9':
                output += i

        m = str(self.degree) + output
        return m


class Skill(models.Model):
    name = models.CharField(primary_key=True, unique=True,
                            max_length=30, auto_created=False,
                            serialize=False, verbose_name='ID')
    Teacher_set = models.ManyToManyField(to='connect.Teacher',
                                         related_name='skills')


class Teacher(models.Model):
    id = models.OneToOneField(
        to=Profile,
        related_name='teacher',
        to_field='id',
        db_column='id',
        on_delete=models.CASCADE,
        primary_key=True)
    Contact = models.BigIntegerField(blank=True, default=0)
    UpVotes = models.BigIntegerField(blank=True, default=0)
    DownVotes = models.BigIntegerField(blank=True, default=0)
    confidence = models.FloatField(blank=True, default=0)
    Gitname = models.CharField(max_length=100, blank=True, )
    Linkedin = models.CharField(max_length=100, blank=True, )
    email = models.OneToOneField(to='auth.User',
                                 on_delete=models.CASCADE,
                                 related_name='teacher',
                                 to_field='email',
                                 db_column='email')

    def __str__(self):
        return str(self.id)

    def get_roll_number(self):
        x = str(self.id)
        output = ""
        for i in x:
            if i == 'B' or i == 'M':
                output += i
            if '0' <= i <= '9':
                output += i
        return output

    # def save(self, *args, **kwargs):
    #     iid = self.get_roll_number()
    #     b = Profile.objects.get(id=iid)
    #     if b.IsTeacher is False:
    #         b.IsTeacher = True
    #         person = {
    #             "Id": b.id,
    #             "Name": b.First_Name + " " + b.Last_Name,
    #             "Email": str((b.email).email)
    #             }
    #         new_teacher_email(person)
    #         b.save()
    #     super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        iid = self.get_roll_number()
        b = Profile.objects.get(id=iid)
        b.IsTeacher = False
        b.save()
        print("yes this delete is getting called", flush=True)
        super().delete(*args, **kwargs)
