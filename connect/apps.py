from django.apps import AppConfig
from connect.models import Teacher
from django.db.models.signals import post_save, post_delete
from connect.signals import profile_isteacher_false, profile_isteacher_true


class ConnectConfig(AppConfig):
    name = 'connect'

    def ready(self):
        post_save.connect(profile_isteacher_true, sender=Teacher)
        post_delete.connect(profile_isteacher_false, sender=Teacher)
