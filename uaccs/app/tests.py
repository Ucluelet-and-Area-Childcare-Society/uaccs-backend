from django.test import TestCase
from .models import Staff, Child, Parent, Resource
from django.core.files.uploadedfile import SimpleUploadedFile

# FOR TESTING OF STAFF BIO
BIO = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. " \
    "Maecenas turpis libero, ornare in augue vulputate, auctor accumsan nunc. " \
    "Phasellus vulputate scelerisque nisi in imperdiet. " \
    "Nam cursus nisl nec justo bibendum, in facilisis odio mattis. " \
    "Pellentesque hendrerit a neque vitae aliquam."


# Tests for staff model
class StaffTestCase(TestCase):
    def setUp(self):
        Staff.objects.create(name="Jack Sparrow", 
                             email="test@gmail.com", 
                             role="Director",
                             bio=BIO,
                             photo = )

# Tests for child model
class ChildTestCase(TestCase):
    pass

# Tests for parent model
class ParentTestCase(TestCase):
    pass

# Tests for resource model
class ResourceTestCase(TestCase):
    pass