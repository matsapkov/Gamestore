from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField("email address", blank=False, unique=True, null=False)
    image = models.ImageField(upload_to='users_images', null=True, blank=True)

