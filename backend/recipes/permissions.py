from rest_framework import permissions


class IsAuthorOrAdminOrReadOnly(permissions.BasePermission):
    """Класс определения прав доступа."""

    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.is_authenticated
        return True

    def has_object_permission(self, request, view, local_obj):
        if request.user.is_authenticated:
            return (
                request.user.is_superuser
                or local_obj.author == request.user
                or request.method == 'POST'
            )
        return request.method in permissions.SAFE_METHODS
