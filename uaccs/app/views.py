from rest_framework import viewsets
from .models import Staff, Parent, Child, Resource
from .serializers import StaffSerializer, ParentSerializer, ChildSerializer, ResourceSerializer


# Note: Viewset automatically provides: 'list', 'create', 'retrieve', 'update', 'delete' 

## Staff View Set
class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer