import uuid

from django.core.validators import MinValueValidator
from django.db import models
from django.utils.timezone import now

from website.models import User, Group


class Cost(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    description = models.CharField(max_length=200)
    amount = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    members = models.ManyToManyField(to=User, related_name='shared_costs')
    paid_by = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='paid_costs')
    date = models.DateField(default=now)
    image = models.ImageField(upload_to='cost-images', null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    group = models.ForeignKey(to=Group, on_delete=models.CASCADE, related_name='costs_set')
    archived = models.BooleanField(default=False)

    # ToDo: Category and Split Type

    def __str__(self):
        return f"{self.description} in {self.group}"
