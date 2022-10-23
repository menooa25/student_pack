from rest_framework.permissions import BasePermission, SAFE_METHODS

from accounts.models import Account


class IsTeacherOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return request.user.role == Account.TEACHER

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.method != 'PUT' and request.user.is_authenticated:
            return request.user.role == Account.TEACHER
