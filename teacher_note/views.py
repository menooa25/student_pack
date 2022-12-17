from rest_framework.viewsets import ModelViewSet

from lessons.permisions import IsTeacherOrReadOnly
from teacher_note.models import Note
from teacher_note.permisions import OnlyTeacherLessons
from teacher_note.serializers import NoteSerializer


class NoteViewSet(ModelViewSet):
    serializer_class = NoteSerializer
    permission_classes = [IsTeacherOrReadOnly,OnlyTeacherLessons ]
    def get_queryset(self):
        queryset = Note.objects.all()
        user = self.request.user
        if user.is_authenticated:
            return queryset.filter(teacher=user)
        return queryset

    def get_serializer_context(self):
        return {'user': self.request.user}

