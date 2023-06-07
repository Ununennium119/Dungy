import uuid

from django.db import models

from website.models import User


class Transaction(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    from_user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='from_transactions_set')
    to_user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='to_transactions_set')
    amount = models.FloatField()

    def __str__(self):
        return f'{self.amount} from {self.from_user.username} to {self.to_user.username}'
