from rest_framework import permissions

#TODO переделать под только авторизованного пользователя
class IsOwner(permissions.BasePermission):
    """
    Только пользователь может редактировать
    """
    def has_object_permission(self, request, view, obj):
        # if request.method in permissions.SAFE_METHODS:
        #     return True
        return obj.user == request.user