from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrEngineer(BasePermission):
    """Allows access only to users with the ADMIN role."""

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == 'ADMIN'
        )


class IsClinicalOrReadOnly(BasePermission):
    """Allows read-only access to CLINICAL users; full access to ADMIN users."""

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.method in SAFE_METHODS:
            return True
        return request.user.role == 'ADMIN'
