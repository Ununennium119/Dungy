import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=16, null=True, blank=True)

    def __str__(self):
        return str(self.username)
