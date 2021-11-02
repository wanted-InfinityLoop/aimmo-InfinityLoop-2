from django.db import models
from core.models import AbstractTimeStamped


class User(AbstractTimeStamped):
    name = models.CharField(max_length=32, null=True)
    email = models.CharField(max_length=64, unique=True)
    password = models.CharField(max_length=128, null=True)

    class Meta:
        db_table = "users"
