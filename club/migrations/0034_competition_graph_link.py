# Generated by Django 3.2.10 on 2022-01-09 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('club', '0033_alter_competition_faq'),
    ]

    operations = [
        migrations.AddField(
            model_name='competition',
            name='graph_link',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
