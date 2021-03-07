from django.db import models
from django.contrib.auth.models import AbstractUser


# -----------------------------------------------------------------------------
# User
# -----------------------------------------------------------------------------
class User(AbstractUser):
    """
    User based on the abstract base class that implements a fully
    featured User model with admin-compliant permissions.

    Username and password are required. Other fields are optional.
    """

    relate_activities = models.BooleanField(default=True)

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)

    def has_read_permission(self, user):
        return user.is_staff or self.id == user.id

    def has_write_permission(self, user):
        """IMPORTANT: Only staff users can edit data from users."""
        return user.is_staff

