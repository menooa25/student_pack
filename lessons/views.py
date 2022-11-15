from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from accounts.models import Account

from lessons.models import Lesson, Building, Status
from lessons.permisions import IsTeacherOrReadOnly
from lessons.serializers import LessonSerializer, BuildingSerializer, StatusSerializer, UserSerializer


class LessonViewSet(ModelViewSet):
    permission_classes = [IsTeacherOrReadOnly]
    serializer_class = LessonSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_fields = ['name', 'status', 'lesson_day', 'building__id', 'teacher__id']
    search_fields = ['teacher__name', 'name', 'building__name', 'status__name', 'lesson_day', 'lesson_time']

    def get_queryset(self):
        queryset = Lesson.objects.all().select_related('building', 'status').prefetch_related('teacher')
        user = self.request.user
        if user.is_authenticated:
            return queryset.filter(teacher=user)
        return queryset

    def get_serializer_context(self):
        return {'user': self.request.user}

    @action(detail=False)
    def filter_options(self, request):
        building_serializer = BuildingSerializer(Building.objects.all(), many=True)
        status_serializer = StatusSerializer(Status.objects.all(), many=True)
        teacher_serializer = UserSerializer(get_user_model().objects.filter(role=Account.TEACHER), many=True)

        return Response(
            {
                'building': building_serializer.data,
                'status': status_serializer.data,
                'teacher': teacher_serializer.data
            },
            status.HTTP_200_OK)
