from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ConnectConfig(AppConfig):
    name = 'connect'
    verbose_name = _('connect')

    def ready(self):
        from . import signals
        signals.varia()
