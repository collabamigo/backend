# Generated by Django 3.2.9 on 2021-11-30 15:44

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('form', '0003_auto_20210919_0614'),
    ]

    operations = [
        migrations.AddField(
            model_name='form',
            name='closes_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='form',
            name='opens_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]