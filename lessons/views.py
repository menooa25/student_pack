from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet

from lessons.models import Lesson
from lessons.permisions import IsTeacherOrReadOnly
from lessons.serializers import LessonSerializer


class LessonViewSet(ModelViewSet):
    permission_classes = [IsTeacherOrReadOnly]
    serializer_class = LessonSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_fields = ['name', 'status', 'lesson_day', 'building__id', 'teacher__id']
    search_fields = ['teacher__name', 'name', 'building__name', 'status__name', 'lesson_day', 'lesson_time']

    def get_queryset(self):
        queryset = Lesson.objects.all()
        user = self.request.user
        if user.is_authenticated:
            return queryset.filter(teacher=user)
        return queryset

    def get_serializer_context(self):
        return {'user': self.request.user}
