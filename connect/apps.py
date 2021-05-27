from django.apps import AppConfig
from django.db.models.signals import post_save, post_delete
from django.utils.translation import ugettext_lazy as _
from connect.signals import profile_isteacher_false, profile_isteacher_true


class ConnectConfig(AppConfig):
    name = 'connect'
    verbose_name = _('connect')

    def ready(self):
        from connect.models import Teacher
        post_save.connect(profile_isteacher_true, sender=Teacher)
        post_delete.connect(profile_isteacher_false, sender=Teacher)
