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
    email = models.EmailField(max_length=254)
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


# Resource Model (for generic site resources, i.e. photos, urls etc)
class Resource(TimeStampedModel):
    """
    model to store generic website resources that dont fall into above models.
    Anything like photos, files, URLS, other static web resources on the site.
    All file types are optional, but atleast one must be present in object instantiation.
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
        if self.url == None and self.image == None and self.file == None:
            raise ValidationError("atleast one resource type must be chosen. ")

# User model for future user authentication needs
class User(AbstractUser):
    pass        # add when necessary
    



