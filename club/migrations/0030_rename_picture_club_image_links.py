# Generated by Django 3.2.10 on 2021-12-25 18:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('club', '0029_alter_competitionwinner_position'),
    ]

    operations = [
        migrations.RenameField(
            model_name='club',
            old_name='picture',
            new_name='image_links',
        ),
    ]
