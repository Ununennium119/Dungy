import uuid

from django.apps import apps
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Sum, FloatField, F, ExpressionWrapper, Count


class User(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    email = models.EmailField(unique=True)
    balance = models.FloatField(default=0.0)
    friends = models.ManyToManyField(to='User', blank=True)

    def __str__(self):
        return str(self.username)

    @property
    def debt(self) -> float:
        return self.cost_members_set.filter(paid=False).exclude(cost__paid_by=self).annotate(
            members_count=Count('cost__members_set')).annotate(
            amount=ExpressionWrapper(F('cost__amount') / F('members_count'), output_field=FloatField())).aggregate(
            debt=Sum('amount')).get('debt', 0.0)

    @property
    def credit(self) -> float:
        return apps.get_model('website.CostMember').objects.filter(paid=False, cost__paid_by=self).exclude(user=self).annotate(
            members_count=Count('cost__members_set')).annotate(
            amount=ExpressionWrapper(F('cost__amount') / F('members_count'), output_field=FloatField())).aggregate(
            credit=Sum('amount')).get('credit', 0.0)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
