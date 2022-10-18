from django.contrib import admin

from lessons.models import Lesson, Building, Status


class LessonAdmin(admin.ModelAdmin):
    list_display = ['name', 'lesson_day', 'lesson_time', 'teacher', 'updated_at']
    search_fields = ['name', 'teacher__name', 'teacher__username', 'lesson_time', 'lesson_day']


admin.site.register(Lesson, LessonAdmin)
admin.site.register(Building)
admin.site.register(Status)
