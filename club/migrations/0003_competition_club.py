# Generated by Django 3.2.6 on 2021-08-31 10:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('club', '0002_alter_social_other'),
    ]

    operations = [
        migrations.AddField(
            model_name='competition',
            name='club',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='club.club'),
        ),
    ]