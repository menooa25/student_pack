from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Building(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Status(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    SHANBE = 0
    YEKSHANBE = 1
    DOSHANBE = 2
    SESHANBE = 3
    CHAHARSHANBE = 4
    PANJSHANBE = 5
    JOME = 6
    WEEK_DAYS = [
        (SHANBE, 'شنبه'),
        (YEKSHANBE, 'یکشنبه'),
        (DOSHANBE, 'دوشنبه'),
        (SESHANBE, 'سه‌شنبه'),
        (CHAHARSHANBE, 'چهارشنبه'),
        (PANJSHANBE, 'پنجشنبه'),
        (JOME, 'جمعه'),
    ]
    name = models.CharField(max_length=200)
    lesson_time = models.TimeField()
    lesson_day = models.IntegerField(choices=WEEK_DAYS)
    class_number = models.IntegerField(default=None, null=True)
    building = models.ForeignKey(Building, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = ('lesson_time', 'lesson_day', 'teacher', 'name')

    def __str__(self):
        return self.name
