
from rest_framework import permissions, exceptions
from .models import Club


class IsClubOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow club admins to modify their club.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff or request.method in permissions.SAFE_METHODS:
            return True
        elif isinstance(obj, Club) and obj.admins.filter(pk=request.user.pk).exists():
            return True
        elif hasattr(obj, "club") and obj.club.admins.filter(pk=request.user.pk).exists():
            return True
        else:
            raise exceptions.PermissionDenied()


class IsClubOwner(permissions.BasePermission):
    """
    Custom permission to only allow club admins to modify their club.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.clubs.exists())

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        elif isinstance(obj, Club) and obj.admins.filter(pk=request.user.pk).exists():
            return True
        elif hasattr(obj, "club") and obj.club.admins.filter(pk=request.user.pk).exists():
            return True
        else:
            raise exceptions.PermissionDenied()
