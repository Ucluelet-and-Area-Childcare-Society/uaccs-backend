from rest_framework.permissions import BasePermission, SAFE_METHODS

# Custom Permission ReadOnly
class ReadOnly(BasePermission):
    def has_permission(self, request, view): # type: ignore
        return request.method in SAFE_METHODS


# Custom Permission CreateOnly
class CreateOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method == 'POST'
