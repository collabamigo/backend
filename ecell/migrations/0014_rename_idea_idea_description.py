# Generated by Django 3.2.10 on 2022-02-06 10:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecell', '0013_auto_20220206_1419'),
    ]

    operations = [
        migrations.RenameField(
            model_name='idea',
            old_name='idea',
            new_name='description',
        ),
    ]