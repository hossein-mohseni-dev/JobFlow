from rest_framework.permissions import BasePermission


class IsEmailVerified(BasePermission):
    message = "Verify your email before using this action."

    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and getattr(user.profile, "email_verified", False))
