from django.db import models


# TimeStampedModel (base class)
class TimeStampedModel(models.Model):
    """
    Abstract base class that tracks when models are created and updated
    (useful for debudding)
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
    pass

# Child Model (Many-to-Many Relationship with Parent)
class Child(TimeStampedModel):
    """
    Model defines the following attributes:
        - name
        - date of birth (date field)
        - parent(s) names
        - parent(s) phone numbers
        - parent(s) email addresses
        - starting date (date childcare required)"""
    pass


# Parent Model (Many-to-Many Relationship with Child)
class Parent(TimeStampedModel):
    """
    model defines the following attributes:
        - name
        - phone number
        - email address
        - child(s) names
    """
    pass

# Resource Model (for generic site resources, i.e. photos, urls etc)
class Resource(TimeStampedModel):
    """
    model to store generic website resources that dont fall into above models.
    Anything like photos, files, URLS, other static web resources on the site.
    """
    pass



