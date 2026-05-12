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
    """
    def setUp(self):
        User = get_user_model()
        self.url = reverse('staff-list')
        self.admin = User.objects.create_user(username="director", password="password123", is_staff = True)

        # mimics a normal user interacting with site
        self.non_admin = User.objects.create_user(username = "non_admin", password = "123")
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

        # test PATCH (Partial Update):
        staff = Staff.objects.create(name="staff", bio=BIO, email="staff@gmail.com", 
                                     role="admin", photo=generate_img("i.jpeg", (1, 1), "blue"))
        patch = {"role": "assistant"}
        patch_url = reverse("staff-detail", kwargs= {'pk': staff.pk})
        patch_response = self.client.patch(patch_url, patch, format = "json")
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)

        # Refresh and Verify
        staff.refresh_from_db()
        self.assertEqual(staff.role, "assistant")
        self.assertEqual(staff.name, "staff")
    
    def test_non_admin_failure(self):
        # attempt GET and POST
        self.client.force_authenticate(user = self.non_admin)   # type: ignore # change auth to non_admin
        response = self.client.post(self.url, self.data, format = "multipart")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        get = self.client.get(self.url)
        self.assertEqual(get.status_code, status.HTTP_403_FORBIDDEN)




class RegistrationTest(APITestCase):
    """Registration tests need to check:
        - non-admin can only create records
        - admin can do full CRUD 
    """
    def setUp(self):
        User = get_user_model()
        self.url = reverse("child-list")
        self.client = APIClient()
        self.admin = User.objects.create_user(username="director", password="password123", is_staff = True)
        self.client.force_authenticate(user = self.admin)

        # mimics a normal user interacting with site
        self.non_admin = User.objects.create_user(username = "non_admin", password = "123")

        self.data = {
            "name": "Tommy Pickles",
            "dob": "2024-01-01",
            "starting_date": "2026-09-01",
            "parents": [
                {
                "name": "Stu Pickles",
                "phone_number": "+16502530000",
                "email": "stu@inventor.com"
                },
                {
                "name": "Didi Pickles",
                "phone_number": "+12345678900",
                "email": "didi@psych.com"
                }
            ]
        }
    
    def test_parent_create_only(self):
        # only POST should work
        self.client.force_authenticate(user = self.non_admin)   # type: ignore
        response = self.client.post(self.url, self.data, format = "json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Child.objects.count(), 1)
        self.assertEqual(Parent.objects.count(), 2)
        parent = Parent.objects.get(name = "Stu Pickles")
        self.assertTrue(parent.children.filter(name = "Tommy Pickles").exists())    # type: ignore
        
        # Any other Request should fail
        get = self.client.get(self.url)
        self.assertEqual(get.status_code, status.HTTP_403_FORBIDDEN)
        
        delete = self.client.delete(self.url)
        self.assertEqual(delete.status_code, status.HTTP_403_FORBIDDEN)
        
        put = self.client.put(self.url, self.data, format = "json") # replacing with same data here but should still fail
        self.assertEqual(put.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_admin_full_crud(self):
        # All CRUD operations should succeed
        # if POST works without admin, will work with it, no need to retest
        self.client.force_authenticate(user = self.admin)  # type: ignore
        response = self.client.post(self.url, self.data, format = "json")
        
        get = self.client.get(self.url)
        self.assertEqual(get.status_code, status.HTTP_200_OK)
        parent = Parent.objects.get(phone_number = "+16502530000")
        
        new_data = {
            "name": "Tommy Pickles",
            "dob": "2025-01-01",
            "starting_date": "2026-11-01",
            "parents": [
                {
                "id": parent.id,            # type: ignore   
                "name": "Stu Pickles",
                "phone_number": "+16502530000",
                "email": "stu@inventor.com"
                },
            ]
        }
        child = Child.objects.get(name = 'Tommy Pickles')
        put_url = reverse('child-detail', kwargs = {"pk": child.pk})
        put = self.client.put(put_url, new_data, format = "json")
        self.assertEqual(put.status_code, status.HTTP_200_OK)
        
        child.refresh_from_db()
        self.assertEqual(child.parents.count(), 1)  # note PUT/ PATCH does not delete from db
        self.assertEqual(str(child.dob), "2025-01-01")   # instead of 2024-01-01
        
        # Note: Delete Parents if NO CHILD LINKED??
        
        delete_url = reverse('child-detail', kwargs = {"pk": child.pk})
        delete = self.client.delete(delete_url)
        self.assertEqual(delete.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Child.objects.filter(name = "Tommy Pickles").exists())
        
        
        
        
        


class ResourceTest(APITestCase):
    pass


# delete temp directory
tearDownModule()