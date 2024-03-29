# Generated by Django 3.2.3 on 2021-05-26 03:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('connect', '0009_alter_skill_teacher_set'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='teacher',
            options={},
        ),
        migrations.AddField(
            model_name='teacher',
            name='Gitname',
            field=models.CharField(blank=True, default='NA', max_length=100),
        ),
        migrations.AddField(
            model_name='teacher',
            name='Linkedin',
            field=models.CharField(blank=True, default='NA', max_length=100),
        ),
        migrations.AddField(
            model_name='teacher',
            name='email',
            field=models.OneToOneField(db_column='email', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='teacher', to=settings.AUTH_USER_MODEL, to_field='email'),
        ),
    ]
