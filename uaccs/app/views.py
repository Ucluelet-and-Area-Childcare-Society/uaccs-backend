from rest_framework import viewsets, mixins
from .models import Staff, Parent, Child, Resource
from .serializers import StaffSerializer, ParentSerializer, ChildSerializer, ResourceSerializer
from rest_framework.permissions import IsAdminUser
from .permissions import ReadOnly

# Note: Viewset automatically provides: 'list', 'create', 'retrieve', 'update', 'delete' 

## Staff View Set: INTERNAL ADMIN ONLY
class StaffViewSet(viewsets.ModelViewSet):
    """
    permissions set to IsAdminUser, CRUD operations only permitted
    to Administrators, else throws exception: 403 FORBIDDEN
    """
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    permission_classes = [IsAdminUser]


# Resource View Set: Public Download, Private Access
class ResourceViewSet(viewsets.ModelViewSet):
    """
    Permission set to IsAdminUserOrReadOnly, CRUD permitted for Admins,
    everyone else is ReadOnly.
    """
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    permission_classes = [IsAdminUser | ReadOnly]