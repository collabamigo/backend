import os
from django.core.mail import send_mail
EMAIL_HOST_USER = os.getenv("EMAIL")


def registration_email(reciever):
    Subject = "Welcome To Collabconnect"
    Message = "Hi " + reciever["Name"] + \
        ". You have been registered as "\
        + reciever["Id"] + "."
    email = reciever["Email"]
    send_mail(Subject, Message, EMAIL_HOST_USER,
              [email], fail_silently=False)
    return True


def new_teacher_email(reciever):
    Subject = "Welcome To Collabconnect"
    Message = "Hi " + reciever["Name"] + \
        ". You have been registered as teacher "\
        + reciever["Id"] + "."
    email = reciever["Email"]
    send_mail(Subject, Message, EMAIL_HOST_USER,
              [email], fail_silently=False)
    return True
