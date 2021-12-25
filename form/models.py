from django.db import models
from django.core.exceptions import ValidationError
from club.models import Competition


def file_size_limit(value):
    limit = 10 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 10 MiB.')


class Form(models.Model):
    id = models.AutoField(primary_key=True)
    # edit_after_submit = models.BooleanField(default=False)
    confirmation_message = models.TextField(max_length=100,
                                            default="Your response has been "
                                                    "recorded.")
    # is_quiz = models.BooleanField(default=False)
    # allow_view_score = models.BooleanField(default=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    collect_email = models.BooleanField(default=True)
    competition = models.OneToOneField(Competition,
                                       related_name="form",
                                       on_delete=models.CASCADE)
    skeleton = models.TextField()  # This will be a manual-serialized JSONArray
    opens_at = models.DateTimeField()
    closes_at = models.DateTimeField(blank=True, null=True)
    allow_multiple_submissions = models.BooleanField(default=False)


# need to fix this tomorrow
class FormResponse(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE,
                             related_name="responses")
    responders = models.ManyToManyField(to="auth.User")


class ResponseElement(models.Model):
    # To be used for: Text, Email, Number, MCQ
    parent = models.ForeignKey(FormResponse, related_name="ResponseElements",
                               on_delete=models.CASCADE)
    question = models.CharField(max_length=15)
    value = models.TextField(blank=True)
