
from rest_framework import permissions, exceptions
from .models import Club, Competition


class IsClubOwner(permissions.BasePermission):
    """
    Custom permission to only allow club admins to modify their club.
    """

    def has_permission(self, request, view, club_requested: Club = None):
        post_flag = True
        if request.method == "POST":
            if club_requested is None:
                print(request.data)
                club = request.data.get("club")
                if club is None:
                    club = request.data.get("clubs")[0]
                club_requested = Club.objects.get(username=club)
            post_flag = club_requested.admins.filter(pk=request.user.pk).exists()
        print(bool(post_flag and request.user and request.user.is_authenticated))
        return bool(post_flag and request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj, club_requested: Club = None):
        if request.user.is_superuser:
            return True
        elif club_requested is not None:
            if club_requested.admins.filter(pk=request.user.pk).exists():
                return True
            else:
                return False
        elif isinstance(obj, Club) and obj.admins.filter(pk=request.user.pk).exists():
            return True
        elif hasattr(obj, "club") and obj.club.admins.filter(pk=request.user.pk).exists():
            return True
        elif hasattr(obj, "clubs") and obj.clubs.filter(admins__pk=request.user.pk).exists():
            return True
        else:
            raise exceptions.PermissionDenied()


class IsClubOwnerOrReadOnly(IsClubOwner):
    """
    Custom permission to only allow club admins to modify their club.
    """

    def has_object_permission(self, request, view, obj, **kwargs):
        return request.method in permissions.SAFE_METHODS or super().has_object_permission(request, view, obj)


class CompetitionWinnerPermission(IsClubOwner):

    def has_permission(self, request, view, club_requested: str = None):
        competition_requested = request.data.get("competition")
        return super().has_permission(request, view, Competition.objects.get(pk=competition_requested).clubs.all()[0])

    def has_object_permission(self, request, view, obj, **kwargs):
        return super().has_object_permission(request, view, obj.competition.clubs.all()[0])


class IsClubMember(permissions.BasePermission):
    """
    Custom permission to only allow club members to modify their club.
    """

    def has_permission(self, request, view, club_requested: Club = None):
        post_flag = True
        if request.method == "POST":
            if club_requested is None:
                print(request.data)
                club = request.data.get("club")
                if club is None:
                    club = request.data.get("clubs")[0]
                club_requested = Club.objects.get(username=club)
            post_flag = club_requested.members.filter(pk=request.user.pk).exists()
        print(bool(post_flag and request.user and request.user.is_authenticated))
        return bool(post_flag and request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj, club_requested: Club = None):
        if request.user.is_superuser:
            return True
        elif club_requested is not None:
            if club_requested.members.filter(pk=request.user.pk).exists():
                return True
            else:
                return False
        elif isinstance(obj, Club) and obj.members.filter(pk=request.user.pk).exists():
            return True
        elif hasattr(obj, "club") and obj.club.members.filter(pk=request.user.pk).exists():
            return True
        elif hasattr(obj, "clubs") and obj.clubs.filter(members__pk=request.user.pk).exists():
            return True
        else:
            raise exceptions.PermissionDenied()


class IsClubMemberOrReadOnly(IsClubMember):
    """
    Custom permission to only allow club members to modify their club.
    """

    def has_object_permission(self, request, view, obj, **kwargs):
        return request.method in permissions.SAFE_METHODS or super().has_object_permission(request, view, obj)
