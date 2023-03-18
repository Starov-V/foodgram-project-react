from enum import Enum

from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            is_superuser = request.user.is_superuser
            is_admin = request.user.is_admin
            return is_admin or is_superuser
        return False


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        is_superuser = request.user.is_superuser
        is_admin = (
            request.user.is_authenticated
            and request.user.is_admin
        )
        return is_admin or is_superuser


class IsAuthor(BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
