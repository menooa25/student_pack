from django.contrib.auth import get_user_model
from rest_framework import serializers

from lessons.models import Lesson, Building, Status


class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = ['name', 'id']


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ['name', 'id']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['name', 'id']


class LessonSerializer(serializers.ModelSerializer):
    building_name = serializers.SlugRelatedField(slug_field='name',
                                                 source='building', read_only=True)
    status_name = serializers.SlugRelatedField(slug_field='name',
                                               source='status', read_only=True)
    teacher = serializers.SlugRelatedField(slug_field='name', read_only=True)
    building = serializers.PrimaryKeyRelatedField(write_only=True,queryset=Building.objects.all())
    status = serializers.PrimaryKeyRelatedField(write_only=True,queryset=Status.objects.all())

    class Meta:
        model = Lesson
        fields = [
            'name',
            'lesson_time',
            'lesson_day',
            'building',
            'building_name',
            'created_at',
            'updated_at',
            'teacher',
            'status',
            'status_name',
            'id'
        ]

    def validate(self, attrs):
        dict_attrs = dict(attrs)
        user = self.context.get('user')
        lesson_time = dict_attrs.get('lesson_time')
        lesson_day = dict_attrs.get('lesson_day')
        name = dict_attrs.get('name')
        lesson = self.Meta.model.objects.filter(teacher=user, lesson_time=lesson_time, lesson_day=lesson_day,
                                                name=name).first()
        if lesson:
            message = f'The fields users, lesson_time, lesson_day and name must make a unique set.'
            raise serializers.ValidationError({'unique_together': message})
        return attrs

    def create(self, validated_data):
        user = self.context.get('user')
        return Lesson.objects.create(**validated_data, teacher=user)
