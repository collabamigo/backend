from django.db.models.signals import post_save
from django.dispatch import receiver

from backend import settings
from connect import email_templates
from connect.models import Profile, Teacher
from connect.emailhandler import send_mail


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
def teacher_creation(sender, instance: Teacher, created, **kwargs):
    if created:
        format_dict = {
            'receiverName': instance.email.profile.First_Name,
            'frontend': settings.FRONTEND_URL,
        }
        send_mail(to=[instance.email.email],
                  subject="We appreciate your initiative to help others",
                  body=email_templates.teacher_welcome_text.
                  format(**format_dict),
                  html=email_templates.teacher_welcome_html.
                  format(**format_dict))
