from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        if request.user:
            if request.user.is_staff:
                return True
            else:
                return obj.email == request.user
        else:
            return False


class IsAdminOrReadOnlyIfAuthenticated(permissions.BasePermission):
    """
    Custom permission to only allow authenticated requests to read and admin requests to write
    """
    def has_object_permission(self, request, view, obj):
        if request.user:
            if request.user.is_staff:
                return True
            else:
                return request.method in permissions.SAFE_METHODS
        else:
            return False
