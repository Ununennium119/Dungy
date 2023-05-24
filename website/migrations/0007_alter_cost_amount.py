# Generated by Django 4.2 on 2023-05-06 10:23

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0006_alter_cost_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cost',
            name='amount',
            field=models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
    ]