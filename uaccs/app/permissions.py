from rest_framework.permissions import BasePermission, SAFE_METHODS

# Custom Permission Logic ReadOnly
class ReadOnly(BasePermission):
    def has_permission(self, request, view): # type: ignore
        return request.method in SAFE_METHODS
