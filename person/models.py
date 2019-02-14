from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta

# Create your models here.

class setter_request(models.Model):
    username = models.CharField(max_length=50)
    description = models.TextField()
    date_submitted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class challenge(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=(('O', 'Open'), ('P', 'Private'),), default='O')
    slug = models.SlugField(max_length=50)
    status = models.CharField(max_length=15, choices=(('M', 'Making'), ('A', 'Active'), ('C', 'Completed'),), default='M')
    start_date = models.DateField(default=timezone.now() + timedelta(days=1))
    end_date = models.DateField(default=timezone.now() + timedelta(days=1) + timedelta(hours=3))
    start_time = models.TimeField(default=timezone.now() + timedelta(days=1))
    end_time = models.TimeField(default=timezone.now() + timedelta(days=1) + timedelta(hours=3))
    instructions = models.CharField(max_length=2000, default='None')

    def __str__(self):
        return self.name

class challenge_setter(models.Model):
    slug = models.SlugField(max_length=50)
    setter = models.CharField(max_length=50)

    def __str__(self):
        return self.slug

class question(models.Model):
    name = models.CharField(max_length=100)
    challenge_slug = models.CharField(max_length=100)
    slug = models.SlugField(max_length=50)
    points = models.IntegerField()
    difficulty = models.CharField(max_length=8, choices=(('E', 'Easy'), ('M', 'Medium'), ('H', 'Hard'),), default='E')
    statement = models.CharField(max_length=2000)
    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200)
    option4 = models.CharField(max_length=200)
    tags = models.CharField(max_length=250)
    answer = models.CharField(max_length=50, default='')
    editorial = models.CharField(max_length=2000, default='No Editorial provided by the setter.')

    def __str__(self):
        return self.challenge_slug

class submission(models.Model):
    username = models.CharField(max_length=50)
    question_slug = models.SlugField(max_length=50)
    answer = models.CharField(max_length=50, default='')
    challenge = models.CharField(max_length=50)

    def __str__(self):
        return self.username + " - " + self.question_slug

class score(models.Model):
    username = models.CharField(max_length=50)
    challenge_slug = models.SlugField(max_length=50)
    score = models.IntegerField()
