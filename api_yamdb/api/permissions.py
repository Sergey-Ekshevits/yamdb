from rest_framework import permissions


class IsAuthorAdminModeratorOrReadOnly(permissions.BasePermission):
    """Права доступа: Автор отзыва, модератор или администратор."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        has_permission = (
            request.user.is_authenticated
            and (
                request.user == obj.author
                or request.user.role in ['moderator', 'admin']
            )
        )

        return has_permission
