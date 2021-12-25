# Generated by Django 3.2.6 on 2021-09-16 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='eCell',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('team_name', models.CharField(default='null', max_length=50)),
                ('legal_name', models.CharField(default='null', max_length=50)),
                ('college', models.CharField(default='IIIT-D', max_length=100)),
                ('join_date', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
