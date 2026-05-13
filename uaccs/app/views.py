from rest_framework import viewsets
from .models import Staff, Child, Resource
from .serializers import StaffSerializer, ChildSerializer, ResourceSerializer
from rest_framework.permissions import IsAdminUser
from .permissions import ReadOnly, CreateOnly
from django.core.mail import send_mail

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


## Resource View Set: Public Download, Private Access
class ResourceViewSet(viewsets.ModelViewSet):
    """
    Permission set to IsAdminUserOrReadOnly, CRUD permitted for Admins,
    everyone else is ReadOnly (only SAFE_METHODS allowed)
    """
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    permission_classes = [IsAdminUser | ReadOnly]


## Registration View Set: Public Create (POST), Private Access
class RegistrationViewSet(viewsets.ModelViewSet):
    """
    Permissions set to full CRUD for Admin, only Create for everyone else.
    m2m serialization handled by ChildSerializer.
    """
    queryset = Child.objects.all()
    serializer_class = ChildSerializer
    permission_classes = [IsAdminUser | CreateOnly]

    def perform_create(self, serializer):
        # Save instance to db:
        instance = serializer.save()

        # send mail with waitlist information...
