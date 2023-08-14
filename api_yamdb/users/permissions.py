from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Доступ только для администратора или суперпользователя."""
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.role == 'admin'
                or request.user.is_superuser)
