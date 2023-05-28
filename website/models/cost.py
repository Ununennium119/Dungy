import uuid

from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.utils.timezone import now

from website.models import User, Group, Debt


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

    @staticmethod
    def update_debts(cost: 'Cost', reverse: bool):
        members_count = cost.members.count()
        print(cost.amount)
        print(reverse)
        for member in cost.members.all():
            print(member.username)
            # skip if member is the payer
            if member.id == cost.paid_by.id:
                continue

            # calculate member share in cost
            amount = cost.amount / members_count

            # if update is normal, debt is from payer to member
            # else debt is from member to payer
            try:
                if reverse:
                    debt = member.debts.get(creditor__id=cost.paid_by.id)
                else:
                    debt = member.credits.get(debtor_id=cost.paid_by.id)
            except Debt.DoesNotExist:
                debt = None

            # if there is a debt, subtract cost from it
            if debt:
                if amount > debt.amount:
                    amount -= debt.amount
                    debt.amount = 0.0
                    debt.save()
                else:
                    debt.amount -= amount
                    debt.save()
                    continue

            # if update is normal, debt is from member to payer
            # else debt is from payer to member
            try:
                if reverse:
                    debt = member.credits.get(debtor_id=cost.paid_by.id)
                else:
                    debt = member.debts.get(creditor__id=cost.paid_by.id)
            except Debt.DoesNotExist:
                debt = None

            # if there is a debt, add cost to it
            # otherwise create a new debt
            if debt:
                debt.amount += amount
            else:
                if reverse:
                    debt = Debt(debtor_id=cost.paid_by.id, creditor_id=member.id, amount=amount)
                else:
                    debt = Debt(debtor_id=member.id, creditor_id=cost.paid_by.id, amount=amount)
            debt.save()

    def save(self, *args, **kwargs):
        print("-\tSaving...")
        try:
            old_cost = Cost.objects.get(id=self.id)
            Cost.update_debts(old_cost, True)
        except Cost.DoesNotExist:
            pass

        print("-\tCalling super")
        super(Cost, self).save(*args, **kwargs)

        print(self.members)
        print(self.amount)
        print(self.description)
        Cost.update_debts(self, False)


@receiver(m2m_changed, sender=Cost.members.through)
def update_debts(sender, instance, action, **kwargs):
    print("Update debts")
    if action == 'post_add':
        Cost.update_debts(instance, False)
    if action == 'post_remove':
        Cost.update_debts(instance, True)
