# Generated by Django 3.2.10 on 2021-12-30 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('club', '0031_alter_competition_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competition',
            name='link',
            field=models.TextField(blank=True, default='', max_length=100),
        ),
    ]
