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


############################################################################################

class Choices(models.Model):
    choice = models.CharField(max_length=5000)
    is_answer = models.BooleanField(default=False)


class Form(models.Model):
    id = models.IntegerField(primary_key=True, unique=True,
                             max_length=6, auto_created=False,
                             serialize=False, verbose_name='ID')
    entries = models.ForeignKey(Entries.entries_id, on_delete=models.CASCADE)
    edit_after_submit = models.BooleanField(default=False)
    confirmation_message = models.CharField(max_length=10000, default="Your response has been recorded.")
    is_quiz = models.BooleanField(default=False)
    allow_view_score = models.BooleanField(default=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    collect_email = models.BooleanField(default=False)
    # questions = models.ManyToManyField(Questions, related_name="questions")


class Questions(models.Model):
    form_id = models.ForeignKey(Form.id)
    question_id = models.IntegerField(primary_key=True, unique=True,
                                      max_length=6, auto_created=False,
                                      serialize=False, verbose_name='ID')
    question = models.CharField(max_length=10000)
    question_type = models.CharField(max_length=20)
    required = models.BooleanField(default=False)
    answer_key = models.CharField(max_length=5000, blank=True)
    score = models.IntegerField(blank=True, default=0)
    choices = models.ManyToManyField(Choices, related_name="choices")


class Answer(models.Model):
    answer = models.CharField(max_length=5000)
    answer_to = models.ForeignKey(Questions, on_delete=models.CASCADE, related_name="answer_to")


class Responses(models.Model):
    response_to = models.ForeignKey(Form, on_delete=models.CASCADE, related_name="response_to")
    responder_email = models.EmailField(blank=True)
    response = models.ManyToManyField(Answer, related_name="response")
