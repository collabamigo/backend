# Generated by Django 3.2.6 on 2021-08-24 16:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('connect', '0025_auto_20210607_1515'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('answer', models.CharField(max_length=5000)),
            ],
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('choice', models.CharField(default='null', max_length=5000)),
                ('is_answer', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Club',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('link', models.CharField(max_length=100)),
                ('picture', models.CharField(max_length=100)),
                ('college', models.CharField(default='IIIT-D', max_length=100)),
                ('join_date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Competition',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('on_going', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('competition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='club.competition')),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='connect.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Form',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('edit_after_submit', models.BooleanField(default=False)),
                ('confirmation_message', models.TextField(default='Your response has been recorded.', max_length=50)),
                ('is_quiz', models.BooleanField(default=False)),
                ('allow_view_score', models.BooleanField(default=True)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('collect_email', models.BooleanField(default=False)),
                ('entries', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='club.entry')),
            ],
        ),
        migrations.CreateModel(
            name='Social',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('instagram', models.URLField(max_length=100, null=True)),
                ('linkedin', models.URLField(max_length=100, null=True)),
                ('facebook', models.URLField(max_length=100, null=True)),
                ('discord', models.URLField(max_length=100, null=True)),
                ('other', models.URLField(max_length=100)),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='club.club')),
            ],
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('responder_email', models.EmailField(blank=True, max_length=254)),
                ('form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='response', to='club.form')),
                ('response', models.ForeignKey(default='null', on_delete=django.db.models.deletion.CASCADE, related_name='response', to='club.answer')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('question', models.TextField()),
                ('question_type', models.CharField(max_length=20)),
                ('required', models.BooleanField(default=False)),
                ('answer_key', models.TextField(blank=True)),
                ('score', models.IntegerField(blank=True, default=0)),
                ('choices', models.ForeignKey(default='null', on_delete=django.db.models.deletion.CASCADE, related_name='question', to='club.choice')),
                ('form_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='club.form')),
            ],
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answer', to='club.question'),
        ),
    ]
