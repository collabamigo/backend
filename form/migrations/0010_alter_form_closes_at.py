# Generated by Django 3.2.10 on 2021-12-19 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form', '0009_alter_form_collect_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='form',
            name='closes_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]