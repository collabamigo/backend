from django.db import models
from connect.models import Profile


# Create your models here.
class Club(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    link = models.CharField(max_length=100)  # url
    picture = models.CharField(max_length=100)  # url
    college = models.CharField(max_length=100, default="IIIT-D")
    join_date = models.DateField(auto_now_add=True)
    admins = models.ManyToManyField(to="auth.User",
                                    related_name="clubs")


class Social(models.Model):
    id = models.AutoField(primary_key=True)
    club = models.OneToOneField(Club,
                                on_delete=models.CASCADE,
                                related_name="social")
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


##########################################################################
# have to add blank=True


class Choice(models.Model):
    id = models.AutoField(primary_key=True)
    choice = models.CharField(max_length=5000, default='null')
    is_answer = models.BooleanField(default=False)
    # question type and make a new model for type of choices


class Form(models.Model):
    id = models.AutoField(primary_key=True)
    edit_after_submit = models.BooleanField(default=False)
    confirmation_message = models.TextField(max_length=50,
                                            default="Your response has been "
                                                    "recorded.")
    is_quiz = models.BooleanField(default=False)
    allow_view_score = models.BooleanField(default=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    collect_email = models.BooleanField(default=False)
    competition = models.OneToOneField(Competition,
                                       related_name="competition",
                                       on_delete=models.CASCADE)
    # questions = models.ManyToManyField(Questions, related_name="questions")


class Entry(models.Model):
    id = models.AutoField(primary_key=True)
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    participant = models.ForeignKey(Profile, on_delete=models.CASCADE)


class Question(models.Model):
    id = models.AutoField(primary_key=True)
    form_id = models.ForeignKey(Form, on_delete=models.CASCADE)
    question = models.TextField()
    question_type = models.CharField(max_length=20)
    required = models.BooleanField(default=False)
    answer_key = models.TextField(blank=True)
    score = models.IntegerField(blank=True, default=0)
    choices = models.ForeignKey(Choice, related_name="question",
                                on_delete=models.CASCADE, default="null")


class Answer(models.Model):
    id = models.AutoField(primary_key=True)
    answer = models.CharField(max_length=5000)
    question = models.ForeignKey(Question, on_delete=models.CASCADE,
                                 related_name="answer")


class Response(models.Model):
    id = models.AutoField(primary_key=True)
    form = models.ForeignKey(Form, on_delete=models.CASCADE,
                             related_name="response")
    responder_email = models.EmailField(blank=True)
    response = models.ForeignKey(Answer, related_name="response",
                                 on_delete=models.CASCADE, default="null")
