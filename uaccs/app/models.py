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
        - email (might not need now, adding as redundancy)
        - photo (image field url tied to cloud storage)
        - role (i.e. position within the company)
    """
    pass



