from django.db import models


# TimeStampedModel (base class)
class TimeStampedModel(models.Model):
    """
    Abstract base class that tracks when models are created and updated
    (useful for debudding)
    """
    pass

# Staff Model
class Staff(TimeStampedModel):
    """
    Model defines the following attributes:
        - name
        - bio
        - email (might not need now, adding as redundancy) (for internal use only)
        - photo (image field url tied to cloud storage)
        - role (i.e. position within the company)
    """
    pass

# Child Model
class Child(TimeStampedModel):
    """
    Model defines the following attributes:
        - name
        - date of birth (date field)
        - aprent(s) names
        - parent(s) phone numbers
        - parent(s) email addresses
        - starting date (date childcare required)"""
    pass



