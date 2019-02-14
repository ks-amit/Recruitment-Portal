# Generated by Django 2.1 on 2018-10-28 01:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='challenge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('type', models.CharField(choices=[('O', 'Open'), ('P', 'Private')], default='O', max_length=10)),
                ('slug', models.SlugField()),
                ('status', models.CharField(choices=[('M', 'Making'), ('A', 'Active'), ('C', 'Completed')], default='M', max_length=15)),
                ('start_date', models.DateField(default=datetime.datetime(2018, 10, 29, 1, 12, 46, 732086))),
                ('end_date', models.DateField(default=datetime.datetime(2018, 10, 29, 4, 12, 46, 732119))),
                ('start_time', models.TimeField(default=datetime.datetime(2018, 10, 29, 1, 12, 46, 732141))),
                ('end_time', models.TimeField(default=datetime.datetime(2018, 10, 29, 4, 12, 46, 732159))),
                ('instructions', models.CharField(default='None', max_length=2000)),
            ],
        ),
        migrations.CreateModel(
            name='challenge_setter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField()),
                ('setter', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('challenge_slug', models.CharField(max_length=100)),
                ('slug', models.SlugField()),
                ('points', models.IntegerField()),
                ('difficulty', models.CharField(choices=[('E', 'Easy'), ('M', 'Medium'), ('H', 'Hard')], default='E', max_length=8)),
                ('statement', models.CharField(max_length=2000)),
                ('option1', models.CharField(max_length=200)),
                ('option2', models.CharField(max_length=200)),
                ('option3', models.CharField(max_length=200)),
                ('option4', models.CharField(max_length=200)),
                ('tags', models.CharField(max_length=250)),
                ('answer', models.CharField(default='', max_length=50)),
                ('editorial', models.CharField(default='No Editorial provided by the setter.', max_length=2000)),
            ],
        ),
        migrations.CreateModel(
            name='score',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('challenge_slug', models.SlugField()),
                ('score', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='setter_request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('date_submitted', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='submission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('question_slug', models.SlugField()),
                ('answer', models.CharField(default='', max_length=50)),
                ('challenge', models.CharField(max_length=50)),
            ],
        ),
    ]
