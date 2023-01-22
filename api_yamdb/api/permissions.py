from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Предоставление доступа только админу или суперюзеру."""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and (request.user.is_admin or request.user.is_superuser)))


class IsRoleAdmin(permissions.BasePermission):
    """Предоставление доступа только модератору, админу или суперюзеру."""

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.is_admin or request.user.is_staff)

    def has_object_permission(self, request, view, obj):
        return (request.user.is_authenticated
                and (request.user.is_admin or request.user.is_superuser))


class IsAdminOrModeratorOrAuthorOrReadOnly(permissions.BasePermission):
    """
    Предоставление доступа только админу, модератору или автору.
    остальным - только для чтения.
    """
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                or request.user.is_authenticated
                and (request.user.is_admin or request.user.is_moderator))
