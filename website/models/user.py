import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Sum


class User(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    email = models.EmailField(unique=True)
    debt = models.FloatField(default=0.0)
    credit = models.FloatField(default=0.0)
    balance = models.FloatField(default=0.0)
    friends = models.ManyToManyField(to='User')

    def __str__(self):
        return str(self.username)

    def save(self, *args, **kwargs):
        self.debt = self.shared_costs.filter(paid_by__isnull=False).aggregate(Sum('amount'))
        super().save(*args, **kwargs)
