# Generated by Django 3.2.10 on 2022-01-13 10:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('club', '0035_auto_20220113_1449'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='competition',
            options={'ordering': ['-event_start']},
        ),
    ]
