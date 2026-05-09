from rest_framework import viewsets, mixins
from .models import Staff, Parent, Child, Resource
from .serializers import StaffSerializer, ParentSerializer, ChildSerializer, ResourceSerializer
from rest_framework.permissions import IsAdminUser

# Note: Viewset automatically provides: 'list', 'create', 'retrieve', 'update', 'delete' 

## Staff View Set: INTERNAL ADMIN ONLY
class StaffViewSet(viewsets.ModelViewSet):
    """
    permissions set to IsAdminUser, CRUD operations only permitted
    to Administrators, else throws exception.
    """
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    permission_classes = [IsAdminUser]