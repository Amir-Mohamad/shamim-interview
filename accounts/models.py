from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.html import format_html
from .managers import UserManager
# Create your models here.


class User(AbstractUser):
    username = None
    email = models.EmailField(max_length=125, unique=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email
