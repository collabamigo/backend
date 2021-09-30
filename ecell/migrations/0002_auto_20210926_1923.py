# Generated by Django 3.2.7 on 2021-09-26 19:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('connect', '0026_alter_profile_id'),
        ('ecell', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Idea',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('role', models.CharField(choices=[('i', 'ideator'), ('m', 'member')], max_length=8)),
                ('name', models.CharField(default='null', max_length=50)),
                ('idea', models.TextField(max_length=900)),
                ('visibility', models.CharField(choices=[('pub', 'public'), ('priv', 'private')], max_length=10)),
                ('stage', models.CharField(choices=[('i', 'Initiation'), ('p', 'Planning'), ('e', 'Execution'), ('mc', 'Monitoring and Controllling'), ('c', 'Closure')], max_length=40)),
                ('college', models.CharField(default='IIIT-D', max_length=100)),
                ('join_date', models.DateField(auto_now_add=True)),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='connect.profile')),
            ],
        ),
        migrations.DeleteModel(
            name='eCell',
        ),
    ]