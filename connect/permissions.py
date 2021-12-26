from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        else:
            return obj.email == request.user


class IsAdminOrReadOnlyIfAuthenticated(permissions.BasePermission):
    """
    Custom permission to only allow authenticated requests to read
        and admin requests to write
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        else:
            return request.method in permissions.SAFE_METHODS
