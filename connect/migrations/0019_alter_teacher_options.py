# Generated by Django 3.2.3 on 2021-05-29 14:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('connect', '0018_auto_20210529_0717'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='teacher',
            options={'ordering': ['-confidence', '-UpVotes', 'DownVotes']},
        ),
    ]