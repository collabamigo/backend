import os
from django.core import mail

EMAIL_HOST_USER = "CollabConnect <" + os.getenv("EMAIL") + ">"


def registration_email(reciever):
    subject = "Welcome To CollabConnect"
    message = "Hi " + reciever["Name"] + \
              ". You have been registered as " \
              + reciever["Id"] + "."
    email = reciever["Email"]
    send_mail(subject=subject, body=message, to=[email])
    return True


def new_teacher_email(reciever):
    subject = "Welcome To CollabConnect"
    message = "Hi " + reciever["Name"] + \
              ". You have been registered as teacher " \
              + reciever["Id"] + "."
    email = reciever["Email"]
    send_mail(subject=subject, body=message, to=[email])
    return True


def send_mail(to, subject: str = "", body: list = None, html=None):

    if type(to) == str:
        to = [to]
    print("Sending mail to"+", ".join(to))
    mail.send_mail(subject=subject, message=body,
                   from_email=EMAIL_HOST_USER, recipient_list=to,
                   html_message=html)
