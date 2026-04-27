from django.test import TestCase, override_settings
from ..models import Staff, Child, Parent, Resource
from django.core.files.uploadedfile import SimpleUploadedFile
import shutil, tempfile
from PIL import Image
from io import BytesIO
from django.core.exceptions import ValidationError
from datetime import date
from phonenumber_field.phonenumber import PhoneNumber

MEDIA_ROOT = tempfile.mkdtemp() # make temporary directory to store images for tests.
FAKE_FILE = SimpleUploadedFile(name = "file.pdf", content = b"some content here...", content_type= "application/pdf")

# Tests for staff model (all fields are required)
"""
Don't need test for invalid image here since all
images will be passed through Django Serializer / Forms which
automatically validates images.
"""
@override_settings(MEDIA_ROOT = MEDIA_ROOT)
class StaffTestCase(TestCase):
    def setUp(self):
        self.staff = Staff.objects.create(name="Jack Sparrow", 
                             email="test@gmail.com", 
                             role="Director",
                             bio=BIO,
                             photo = generate_img(name="staff_test.jpeg", size=(100, 100), color="green"))
    
    def test_normal_except_img(self):
        """"Test normal values for staff object creation"""
        staff = Staff.objects.get(name="Jack Sparrow")
        self.assertEqual(staff.name, "Jack Sparrow")
        self.assertEqual(staff.email, "test@gmail.com")
        self.assertEqual(staff.role, "Director")
        self.assertEqual(staff.bio, BIO)
        self.assertTrue(staff.photo)
        self.assertEqual(str(staff), staff.name)
    
    def test_name_max_length(self):
        invalid_name = "x" * 76
        # instantiate object without saving to DB
        staff = Staff(name = invalid_name, email = "test@gmail.com", role = "Assistant", bio = "BIOOOO")
        
        with self.assertRaises(ValidationError):
            staff.full_clean()  # should throw a ValidationError

    def test_invalid_email(self):
        invalid_email = "invalid_email"
        staff = Staff(name = "name", email = invalid_email, role = "Caretaker", bio = BIO)
        
        with self.assertRaises(ValidationError):
            staff.full_clean()

    def test_image(self):
       staff = self.staff
       self.assertTrue(staff.photo.url.endswith("staff_test.jpeg"))
       self.assertEqual(staff.photo.width, 100)
       self.assertEqual(staff.photo.height, 100)
       
       with Image.open(staff.photo.path) as img:
           self.assertEqual(img.format, "JPEG")

    def test_required_fields(self):
        staff = Staff(name = "", email = "test@gmail.com", role = "Assistant", bio = "BIOOOO")

        with self.assertRaises(ValidationError):
            staff.full_clean()

    

# Tests for child model
class ChildTestCase(TestCase):
    def setUp(self):
        # Note: this works because .create() doesnt validate Many-Many on creation.
        self.parent1 = Parent.objects.create(
            name = "Parent1",
            phone_number = PhoneNumber.from_string("+12345678900"),
            email = "parent@hotmail.com"
        )

        self.parent2 = Parent.objects.create(
            name = "Parent2",
            phone_number = PhoneNumber.from_string("+98765432100"),
            email = "parent@gmail.com"
        )

        self.child = Child.objects.create(
            name = "child",
            dob = date(2024, 1, 1),
            starting_date = date(2026, 4, 20)
        ) 

    def test_relation(self):
        self.child.parents.add(self.parent1)
        self.child.parents.add(self.parent2)
        self.assertEqual(self.child.parents.count(), 2)
        self.assertIn(self.parent1, self.child.parents.all())
        self.assertIn(self.parent2, self.child.parents.all())
        
        # check reverse relation
        self.assertIn(self.child, self.parent1.children.all())   # type: ignore
        self.assertIn(self.child, self.parent2.children.all())   # type: ignore
        self.assertEqual(self.parent1.children.count(), 1)       # type: ignore
        self.assertEqual(self.parent2.children.count(), 1)       # type: ignore
    
    # Already tested invalid email, required fields, no need to repeat.

    def test_date(self):
        self.assertEqual(self.child.dob, date(2024, 1, 1))
        self.assertEqual(self.child.starting_date, date(2026, 4, 20))

        child2 = Child(name = "c2", dob = "Not a date", starting_date = date(2025, 1, 1))
        with self.assertRaises((ValidationError, TypeError, ValueError)):
            child2.full_clean()

    def test_dob_before_starting_date(self):
        bad_child = Child(name = "name", dob = date(2025, 1, 1), starting_date = date(2023, 1, 1))

        with self.assertRaises(ValidationError):
            bad_child.full_clean()


# Tests for parent model
class ParentTestCase(TestCase):
    def setUp(self):
        self.parent = Parent.objects.create(
            name = "Parent",
            phone_number = PhoneNumber.from_string("+12345678900"),
            email = "parent_email@gmail.com"
        )
    # no need to retest name, email.

    def test_phone_number(self):
        self.assertEqual(self.parent.phone_number, PhoneNumber.from_string("+12345678900"))
        invalid_number = Parent(name = "name", email = "valid@gmail.com", phone_number = "Not A Number")

        with self.assertRaises(ValidationError):
            invalid_number.full_clean()
    
    def test__str__(self):
        self.assertEqual(str(self.parent), self.parent.name)



# Tests for resource model
@override_settings(MEDIA_ROOT = MEDIA_ROOT)
class ResourceTestCase(TestCase):
    def setUp(self):
        self.empty = Resource.objects.create()  # this should fail.

        self.resource_good = Resource.objects.create(url = "https://testurl.com", resource_type = "url")

        self.resource_bad = Resource.objects.create(image = generate_img(name = "test.jpeg", size = (50, 50), color = "blue"), 
                                                    file = FAKE_FILE, 
                                                    resource_type = "image")
    
    # no need to retest image

    def test_url(self):
        self.assertEqual(self.resource_good.url, "https://testurl.com")
        self.assertFalse(self.resource_good.image)
        self.assertFalse(self.resource_good.file)
        self.assertEqual(self.resource_good.resource_type, "url")

    def test_file(self):
        file = Resource(file = FAKE_FILE)    # resource_type defaults to file
        self.assertEqual(file.resource_type, "file")
        self.assertFalse(file.image)
        self.assertFalse(file.url)
        

    def test_resource_mismatch(self):
        pass

    def test_empty(self):
        pass




## ------ HELPER FUNCTIONS FOR TEST CASES BELOW -------


# For testing of staff bios:
BIO = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. " \
    "Maecenas turpis libero, ornare in augue vulputate, auctor accumsan nunc. " \
    "Phasellus vulputate scelerisque nisi in imperdiet. " \
    "Nam cursus nisl nec justo bibendum, in facilisis odio mattis. " \
    "Pellentesque hendrerit a neque vitae aliquam."


# Creates a test image to test the photo fields of above models
# using a SimpleUploadedFile to mock a real image.
def generate_img(name, size, color):
    file_obj = BytesIO()
    img = Image.new(mode = "RGB", size = size, color = color)
    img.save(file_obj, "JPEG")
    file_obj.seek(0)

    return SimpleUploadedFile(
        name = name,
        content = file_obj.read(),
        content_type= "image/jpeg"
    )


## Delete generated temporary directory after all tests have run
def tearDownModule():
    shutil.rmtree(MEDIA_ROOT)


