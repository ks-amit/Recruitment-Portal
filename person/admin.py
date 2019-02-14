from django.contrib import admin
from . import models

# Register your models here.

class SetterRequestAdmin(admin.ModelAdmin):
    readonly_fields = ('username', 'description', 'date_submitted')

admin.site.register(models.setter_request, SetterRequestAdmin)

class ChallengeAdmin(admin.ModelAdmin):
    readonly_fields = ('name', 'slug', 'status', 'type', 'instructions')

admin.site.register(models.challenge, ChallengeAdmin)

class ChallengeSetterAdmin(admin.ModelAdmin):
    readonly_fields = ('slug', 'setter')

admin.site.register(models.challenge_setter, ChallengeSetterAdmin)

class QuestionAdmin(admin.ModelAdmin):
    readonly_fields = ('name', 'slug', 'points', 'difficulty', 'statement', 'option1', 'option2', 'option3', 'option4', 'tags', 'challenge_slug', 'answer', 'editorial')

admin.site.register(models.question, QuestionAdmin)

class SubmissionAdmin(admin.ModelAdmin):
    readonly_fields = ('username', 'question_slug', 'answer', 'challenge')

admin.site.register(models.submission, SubmissionAdmin)

class ScoreAdmin(admin.ModelAdmin):
    readonly_fields = ('username', 'challenge_slug', 'score')

admin.site.register(models.score, ScoreAdmin)
