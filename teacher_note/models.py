from django.contrib.auth import get_user_model
from django.db import models

from lessons.models import Lesson

User = get_user_model()


class Note(models.Model):
    description = models.TextField()
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.teacher} - {self.description}'
