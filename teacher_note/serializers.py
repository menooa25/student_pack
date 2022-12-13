from rest_framework import serializers

from lessons.models import Lesson
from teacher_note.models import Note


class NoteSerializer(serializers.ModelSerializer):
    lesson_id = serializers.PrimaryKeyRelatedField(source='lesson',queryset=Lesson.objects.all() )

    class Meta:
        model = Note
        fields = ['description', 'lesson_id','id']

    def create(self, validated_data):
        user = self.context.get('user')
        note = Note.objects.create(**validated_data,teacher=user)
        return note