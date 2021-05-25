# from django.core.mail import EmailMessage

# email = EmailMessage(
#     'Hello',
#     'Body goes here',
#     'from@example.com',
#     ['to1@example.com', 'to2@example.com'],
#     ['bcc@example.com'],
#     reply_to=['another@example.com'],
#     headers={'Message-ID': 'foo'},
# )
import os
from django.core.mail import send_mail
EMAIL_HOST_USER = os.getenv("EMAIL")


def registration_email(reciever):
    Subject = "Welcome To Collabconnect"
    Message = "Hi " + reciever["Name"] + \
        "You have been registered as "\
        + reciever["Id"] + "."
    email = reciever["Email"] + "@iiitd.ac.in"
    send_mail(Subject, Message, EMAIL_HOST_USER,
              [email], fail_silently=False)
    return True
