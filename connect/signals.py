from django.db.models.signals import post_save
from django.dispatch import receiver

from backend import settings
from connect import email_templates
from connect.models import Profile, Teacher
from connect.emailhandler import new_teacher_email, send_mail


@receiver(post_save, sender=Profile)
def profile_creation(sender, instance: Profile, created, **kwargs):
    if created:
        format_dict = {
            'receiverName': instance.First_Name,
            'frontend': settings.FRONTEND_URL,
        }
        send_mail(to=[instance.email.email],
                  subject="Welcome to CollabConnect",
                  body=email_templates.welcome_email_text.
                  format(**format_dict),
                  html=email_templates.welcome_email_html.
                  format(**format_dict))


@receiver(post_save, sender=Teacher)
def profile_isteacher_true(sender, instance, created, **kwargs):
    if created:
        b = Profile.objects.get(id=str(instance.id))
        person = {
            "Id": b.id,
            "Name": b.First_Name + " " + b.Last_Name,
            "Email": str((b.email).email)
            }
        new_teacher_email(person)


@receiver(post_save, sender=Teacher)
def profile_isteacher_false(sender, instance, **kwargs):
    print(instance.id, flush=True)
    # TODO: Send Remove Email
