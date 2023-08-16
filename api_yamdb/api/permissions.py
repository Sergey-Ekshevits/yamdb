from rest_framework import permissions


class AdminOrReadOnly(permissions.BasePermission):
    """Права доступа: авторизованный администратор."""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (request.user.is_authenticated
                and (request.user.role == 'admin'
                     or request.user.is_superuser))


class IsAuthorAdminModeratorOrReadOnly(permissions.BasePermission):
    """Права доступа: автор отзыва, модератор или администратор."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return (
            request.user.is_authenticated and (
                request.user == obj.author or request.user.role
                in ['moderator', 'admin']
            )
        )
