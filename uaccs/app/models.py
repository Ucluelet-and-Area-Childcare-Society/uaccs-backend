from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser


# TimeStampedModel (base class)
class TimeStampedModel(models.Model):
    """
    Abstract base class that tracks when models are created and updated
    (useful for debugging)
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# Staff Model
class Staff(TimeStampedModel):
    """
    Model defines the following attributes:
        - name
        - bio
        - email (might not need now, adding as redundancy) (for internal use only)
        - photo (image field url tied to cloud storage)
        - role (i.e. position within the company) (choose from set of choices?)
    """
    name = models.CharField(max_length=75)
    bio = models.TextField()
    email = models.EmailField(max_length=254) # might change to be optional later
    role = models.CharField(max_length=100) # may make enumeration for predefined choices
    photo = models.ImageField(upload_to='staff/') # (set up object storage)

    def __str__(self):
        return self.name
    

# Parent Model (Many-to-Many Relationship with Child)
class Parent(TimeStampedModel):
    """
    model defines the following attributes:
        - name
        - phone number
        - email address
        - child(s) names
    """
    name = models.CharField(max_length=75)
    phone_number = PhoneNumberField()
    email = models.EmailField(max_length=254)
    # children already specified Child class, no need to redefine

    def __str__(self):
        return self.name


# Child Model (Many-to-Many Relationship with Parent)
class Child(TimeStampedModel):
    """
    Model defines the following attributes:
        - name
        - date of birth (date field)
        - parent(s) names
        - parent(s) phone numbers
        - parent(s) email addresses
        - starting date (date childcare required)
    """
    name = models.CharField(max_length=75)
    dob = models.DateField()
    starting_date = models.DateField()
    parents = models.ManyToManyField(Parent, related_name='children')

    def __str__(self):
        return self.name
    
    def clean(self):
        super().clean()

        # check if dob is BEFORE starting date
        if self.dob > self.starting_date:
            raise ValidationError("Starting date cannot be after DOB", code="invalid_start_date")

# Resource Model (for generic site resources, i.e. photos, urls etc)
class Resource(TimeStampedModel):
    """
    - Model to store generic website resources that dont fall into above models.

    - Anything like photos, files, URLS, other static web resources on the site.
    All file types are optional, but atleast one must be present in object instantiation.

    - A given resource should only be of one type during object instantiation. 
    (i.e. a resource cannot be a url and image at the same time).

    - Resource Type defaults to file.
    """
    RESOURCE_TYPES = [
        ("url", "URL"),
        ("image", "Image"),
        ("file", "File"),
    ]
    description = models.CharField(max_length=100)
    url = models.URLField(blank=True, null=True)  
    image = models.ImageField(upload_to='resources/images/', null =True, blank =True)
    file = models.FileField(upload_to='resources/files/', null=True, blank=True)
    resource_type = models.CharField(max_length=10, choices=RESOURCE_TYPES, default="file")

    def __str__(self):
        return self.description
    
    # method to ensure atleast one file type is present.
    def clean(self):
        super().clean()

        fields = [self.url, self.image, self.file]
        filled_count = sum(bool(x) for x in fields)

        if filled_count == 0:
            raise ValidationError("atleast one resource type must be chosen. ")
        elif filled_count > 1:
            raise ValidationError("Only one resource type can be set at a time", code = "extra_resource")
        
        if self.resource_type == "url" and not self.url:
            raise ValidationError("Selected URL but did not provide one", code = "resource_mismatch")
        elif self.resource_type == "image" and not self.image:
            raise ValidationError("Selected Image but did not provide one", code = "resource_mismatch")
        elif self.resource_type == "file" and not self.file:
            raise ValidationError("Selected File but did not provide one", code = "resource_mismatch")
        
        # extra check, for redundancy, default type is 'file'
        if not self.resource_type:
            raise ValidationError("Must select a resource type", code = "null_resource_type")
        

# User model for future user authentication needs
class User(AbstractUser):
    pass        # add when necessary
    

# Method to validate resource size to be < 10MB (for all resources)
def validate_resource_size(resource):
    limit = 10 * 1024 * 1024    # equivalent to 10MB

    if resource.size > limit:
        raise ValidationError("This file is too large, please compress it and try again.")
