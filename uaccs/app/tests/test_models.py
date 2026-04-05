from django.test import TestCase
from .models import Staff, Child, Parent, Resource
from django.core.files.uploadedfile import SimpleUploadedFile
import datetime

# FOR TESTING OF STAFF BIO
BIO = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. " \
    "Maecenas turpis libero, ornare in augue vulputate, auctor accumsan nunc. " \
    "Phasellus vulputate scelerisque nisi in imperdiet. " \
    "Nam cursus nisl nec justo bibendum, in facilisis odio mattis. " \
    "Pellentesque hendrerit a neque vitae aliquam."

p1 = 

# Tests for staff model
class StaffTestCase(TestCase):
    def setUp(self):
        Staff.objects.create(name="Jack Sparrow", 
                             email="test@gmail.com", 
                             role="Director",
                             bio=BIO,
                             photo = ...)

# Tests for child model
class ChildTestCase(TestCase):
    def setUp(self):
        Child.objects.create(name="Lionel Messi", 
                             dob = datetime.date(2025, 1, 1),
                             starting_date = datetime.date(2026, 2, 1),
                             parents=p1, p2)

# Tests for parent model
class ParentTestCase(TestCase):
    pass

# Tests for resource model
class ResourceTestCase(TestCase):
    pass