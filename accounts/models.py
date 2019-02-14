from django.db import models

# Create your models here.

USER_CHOICES = (
    ('U', 'standard'),
    ('S', 'setter'),
    ('A', 'admin'),
)

class user(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=200)
    activated = models.BooleanField()
    user_token = models.CharField(max_length=200)
    date_joined = models.DateTimeField(auto_now_add=True)
    user_type = models.CharField(max_length=10, choices=USER_CHOICES, default='U')
    questions_solved = models.IntegerField(default=0, editable=False)
    bio = models.CharField(max_length = 2000, default='')
    contactno = models.IntegerField(max_length=10, blank=True, null=True)
    firstname = models.CharField(max_length=50, default='')
    lastname = models.CharField(max_length=50, default='')
#parag
    image = models.ImageField(upload_to='profile_image', blank=True, null=True)

    def __str__(self):
        return self.username
