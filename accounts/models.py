from django.contrib.auth.models import AbstractUser
from django.db import models


class Account(AbstractUser):
    name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'{self.username} - {self.name}'
