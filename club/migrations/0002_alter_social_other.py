# Generated by Django 3.2.6 on 2021-08-24 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('club', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='social',
            name='other',
            field=models.URLField(max_length=100, null=True),
        ),
    ]
