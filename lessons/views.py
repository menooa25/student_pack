from rest_framework.viewsets import ModelViewSet

from lessons.models import Lesson
from lessons.permisions import IsTeacherOrReadOnly
from lessons.serializers import LessonSerializer


class LessonViewSet(ModelViewSet):
    permission_classes = [IsTeacherOrReadOnly]
    serializer_class = LessonSerializer

    def get_queryset(self):
        queryset = Lesson.objects.all()
        user = self.request.user
        if user.is_authenticated:
            return queryset.filter(teacher=user)
        return queryset

    def get_serializer_context(self):
        return {'user': self.request.user}
