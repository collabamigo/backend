# Generated by Django 3.2.9 on 2021-12-20 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('connect', '0028_alter_profile_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='id',
            field=models.CharField(editable=False, max_length=32, primary_key=True, serialize=False, unique=True),
        ),
    ]