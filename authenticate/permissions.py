
from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class IsTrulyAuthenticated(permissions.BasePermission):
    """
    Custom permission to only allow authenticated users (not dummy user)
    """
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and request.user.email != "dummy.user@collabamigo.com")


class IsTrulyAuthenticatedOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow authenticated users (not dummy user), else read only
    """

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and request.user.is_authenticated and request.user.email != "dummy.user@collabamigo.com")
