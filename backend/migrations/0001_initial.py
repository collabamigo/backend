# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
    ]

    operations = [
        migrations.RunSQL("create unique index unique_auth_user on auth_user(email);")
    ]
