from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    """
    User profile for Google Provider
    """
    provider = 'google'
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_primary = True
    ext_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
