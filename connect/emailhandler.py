import os
from django.core import mail


EMAIL_HOST_USER = "CollabConnect <" + os.getenv("EMAIL") + ">"


def send_mail(to, subject: str = "", body: list = None, html=None):
    if type(to) == str:
        to = [to]
    print("Sending mail to " + ", ".join(to), flush=True)
    mail.send_mail(subject=subject, message=body,
                   from_email=EMAIL_HOST_USER, recipient_list=to,
                   html_message=html)
