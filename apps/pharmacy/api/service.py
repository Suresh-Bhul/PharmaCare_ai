from rest_framework.permissions import BasePermission

class AccessChha(BasePermission):       #Make_own permission_classes

    message = "You Have No Permission"

    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)