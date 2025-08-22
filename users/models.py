from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=20, unique=True)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default_avatar.png')