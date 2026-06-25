from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrEngineer(BasePermission):
    """Bloqueia qualquer requisição de usuários CLINICAL — usado nas operações de escrita."""

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == 'ADMIN'
        )


class IsClinicalOrReadOnly(BasePermission):
    """SAFE_METHODS (GET/HEAD/OPTIONS) liberados para qualquer autenticado; escrita exige ADMIN."""

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.method in SAFE_METHODS:
            return True
        return request.user.role == 'ADMIN'
