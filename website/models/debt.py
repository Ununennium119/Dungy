import uuid

from django.core.validators import MinValueValidator
from django.db import models

from website.models import User


class Debt(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    amount = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    debtor = models.ForeignKey(to=User, related_name='debts', on_delete=models.CASCADE)
    creditor = models.ForeignKey(to=User, related_name='credits', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('debtor', 'creditor')

    def __str__(self):
        return f'{self.debtor.username} owes {self.amount} to {self.creditor.username}'
