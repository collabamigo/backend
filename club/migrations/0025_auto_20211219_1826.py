# Generated by Django 3.2.10 on 2021-12-19 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('club', '0024_alter_club_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='club',
            name='picture',
            field=models.TextField(default='[]'),
        ),
        migrations.AlterField(
            model_name='competition',
            name='image_links',
            field=models.TextField(default='[]'),
        ),
    ]
