from django.db import models
from .User import User


class Group(models.Model):
    class GroupTypes(models.TextChoices):
        APARTMENT = 'AP'
        TRIP = 'TP'
        PARTNER = 'PT'

    id = models.PositiveIntegerField(primary_key=True, auto_created=True)
    title = models.CharField(max_length=200)
    members = models.ManyToManyField(to=User)
    type = models.CharField(max_length=2, choices=GroupTypes.choices, default=GroupTypes.TRIP)

    class Meta:
        unique_together = ('title', 'type')
