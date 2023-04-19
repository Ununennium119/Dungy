import uuid

from django.db import models
from .user import User


class Group(models.Model):
    class GroupTypes(models.TextChoices):
        HOME = 'Home'
        TRIP = 'Trip'
        COUPLE = 'Couple'
        OTHER = 'Other'

    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    name = models.CharField(max_length=200)
    members = models.ManyToManyField(to=User)
    type = models.CharField(max_length=8, choices=GroupTypes.choices, default=GroupTypes.HOME)
    image = models.ImageField(upload_to="group-images", null=True, blank=True)