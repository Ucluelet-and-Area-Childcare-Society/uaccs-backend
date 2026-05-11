from ..models import Staff, Resource, Child, Parent
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from .test_models import generate_img, BIO, tearDownModule
import shutil, tempfile
from django.test import override_settings

# Test API Request Response cycle
MEDIA_ROOT = tempfile.mkdtemp() # make temporary directory to store images for tests.

@override_settings(MEDIA_ROOT = MEDIA_ROOT)
class StaffTest(APITestCase):
    """Staff tests need to check, with correct HTTP status codes:
        - Admin can CRUD staff
        - Non-admin cannot CRUD staff
        - serialization is correct (i.e correct data is passed)"""
    def setUp(self):
        User = get_user_model()
        self.url = reverse('staff-list')
        self.admin = User.objects.create_user(username="director", password="password123", is_staff = True)
        self.non_admin = User.objects.create(username = "non_admin", password = "123")
        self.client = APIClient()
        self.client.force_authenticate(user = self.admin)

        self.data = {
            "name": "testStaff",
            "bio": BIO,
            "email": "test@gmail.com",
            "role": "director",
            "photo": generate_img("img.jpeg", (10, 10), "red")
        }

    def test_staff_crud(self):
        # Note: multipart format is needed to handle image files
        response = self.client.post(self.url, self.data, format = "multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Staff.objects.count(), 1)
        self.assertEqual(Staff.objects.get().name, "testStaff") 
    
    def test_non_admin_failure(self):
        pass
        
    
        



class RegistrationTest(APITestCase):
    pass



class ResourceTest(APITestCase):
    pass


# delete temp directory
tearDownModule()