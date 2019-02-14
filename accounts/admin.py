from django.contrib import admin
from . import models

# Register your models here.

class userAdmin(admin.ModelAdmin):
    readonly_fields = ('date_joined', 'username', 'password', 'user_token', 'activated', 'email', 'questions_solved', 'bio', 'firstname', 'lastname', 'contactno')

admin.site.register(models.user, userAdmin)
