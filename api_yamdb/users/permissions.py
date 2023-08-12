from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Только пользователь может редактировать
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsAdminOrModerator(permissions.BasePermission):
    """
    Доступ только для админов и модераторов
    """

    def has_permission(self, request, view):
        return request.user.role == 'moderator' or request.user.is_staff
