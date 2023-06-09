# Generated by Django 4.2 on 2023-05-28 15:35

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0008_cost_archived'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='balance',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='user',
            name='credit',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='user',
            name='debt',
            field=models.FloatField(default=0.0),
        ),
        migrations.CreateModel(
            name='Debt',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('amount', models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('creditor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='credits', to=settings.AUTH_USER_MODEL)),
                ('debtor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='debts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('debtor', 'creditor')},
            },
        ),
    ]
