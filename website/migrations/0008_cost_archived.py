# Generated by Django 4.2 on 2023-05-27 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0007_alter_cost_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='cost',
            name='archived',
            field=models.BooleanField(default=False),
        ),
    ]