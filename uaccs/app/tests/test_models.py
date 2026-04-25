from django.test import TestCase, override_settings
from ..models import Staff, Child, Parent, Resource
from django.core.files.uploadedfile import SimpleUploadedFile
import datetime
import tempfile
from PIL import Image
from io import BytesIO

MEDIA_ROOT = tempfile.mkdtemp() # make temporary directory to store images for tests.

# Tests for staff model (all fields are required)
@override_settings(MEDIA_ROOT = MEDIA_ROOT)
class StaffTestCase(TestCase):
    def setUp(self):
        Staff.objects.create(name="Jack Sparrow", 
                             email="test@gmail.com", 
                             role="Director",
                             bio=BIO,
                             photo = generate_img(name="staff_test.jpeg", size=(100, 100), color="green"))
        
    def test_normal(self):
        """"Test normal values for staff object creation"""
        staff = Staff.objects.get(name="Jack Sparrow")
        self.assertEqual(staff.name, "Jack Sparrow")
        self.assertEqual(staff.email, "test@gmail.com")
        self.assertEqual(staff.role, "Director")
        self.assertEqual(staff.bio, BIO)
        #self.assertEqual(staff.photo, TEST_IMG)

    

        
        




# Tests for child model
class ChildTestCase(TestCase):
    pass      

# Tests for parent model
class ParentTestCase(TestCase):
    pass

# Tests for resource model
class ResourceTestCase(TestCase):
    pass




## ------ HELPER FUNCTIONS FOR TEST CASES BELOW -------


"""
For Testing of Staff Bios.
"""
BIO = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. " \
    "Maecenas turpis libero, ornare in augue vulputate, auctor accumsan nunc. " \
    "Phasellus vulputate scelerisque nisi in imperdiet. " \
    "Nam cursus nisl nec justo bibendum, in facilisis odio mattis. " \
    "Pellentesque hendrerit a neque vitae aliquam."

"""
Creates a test image to test the photo fields of above models
using a SimpleUploadedFile to mock a real image.
"""
def generate_img(name, size, color):
    file_obj = BytesIO()
    img = Image.new(mode = "RGB", size = size, color = color)
    img.save(file_obj, "JPEG")
    file_obj.seek(0)

    return SimpleUploadedFile(
        name = name,
        content = file_obj.read(),
        content_type= "img/jpeg"
    )

