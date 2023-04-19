from django.db import models


class AdminUser(models.Model):
    id = models.PositiveIntegerField(primary_key=True, auto_created=True)
    username = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200, null=False)