from django.db import models


class User(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    username = models.CharField(max_length=200, null=False, unique=True)
    password = models.CharField(max_length=200, null=False)
    email = models.EmailField()
