# Разрешения для доступа к API
from rest_framework import permissions

class IsManager(permissions.BasePermission):
    """
    Доступ только для пользователей с ролью "Менеджер"
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_manager()
