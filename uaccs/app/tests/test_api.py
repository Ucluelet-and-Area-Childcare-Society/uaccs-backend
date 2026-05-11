from ..models import Staff, Resource, Child, Parent
from rest_framework.test import APITestCase, APIClient, force_authenticate
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User

# Test API Request Response cycle


class StaffTest(APITestCase):
    """Staff tests need to check, with correct HTTP status codes:
        - Admin can CRUD staff
        - Non-admin cannot CRUD staff
        - serialization is correct (i.e correct data is passed)"""
    def setUp(self):
        pass
        



class RegistrationTest(APITestCase):
    pass



class ResourceTest(APITestCase):
    pass