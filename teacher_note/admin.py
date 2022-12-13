from django.contrib import admin

from teacher_note.models import Note

class NoteAdmin(admin.ModelAdmin):
    list_display = ['teacher','description']

admin.site.register(Note,NoteAdmin)