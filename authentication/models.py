from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    github_id = models.CharField(max_length=255, unique=True)
    username = models.CharField(max_length=255)
    avatar_url = models.URLField()
