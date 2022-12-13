from rest_framework.permissions import BasePermission, SAFE_METHODS

from accounts.models import Account
from lessons.models import Lesson


class OnlyTeacherLessons(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST' and request.user.is_authenticated:
            lesson_id = (request.POST.get('lesson_id'))
            user = request.user
            if lesson_id:
                found_count = (Lesson.objects.filter(teacher=user, id=lesson_id).count())
                if found_count == 0:
                    return False
        return True

    def has_object_permission(self, request, view, obj):
        update_methods = ['PATCH', 'PUT']

        if request.method in update_methods:

            if not request.user.is_authenticated:
                return False

            user = request.user
            teacher = obj.teacher
            return teacher.id == user.id
        return True
