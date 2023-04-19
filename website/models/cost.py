import uuid

from django.db import models

from website.models import User


class Cost(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    description = models.TextField(null=False)
    members = models.ManyToManyField(to=User, related_name='shared_costs')
    amount = models.FloatField(default=0.0)
    # split_type = models.TextChoices()
    paid_by = models.OneToOneField(to=User, null=False, on_delete=models.CASCADE, related_name='paid_costs')
    # image = models.ImageField()
    time = models.DateTimeField(null=False)
