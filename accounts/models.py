from django.contrib.auth.models import AbstractUser
from django.db import models


class Account(AbstractUser):
    name = models.CharField(max_length=100, null=True, blank=True)
    TEACHER = 'TCH'
    STUDENT = 'STU'
    ROLES = [
        (TEACHER, 'استاد'),
        (STUDENT, 'دانشجو'),
    ]
    role = models.CharField(choices=ROLES, max_length=30, null=True)

    def __str__(self):
        return f'{self.username} - {self.name}'
