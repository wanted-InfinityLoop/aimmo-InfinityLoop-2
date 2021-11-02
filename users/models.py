from django.db import models


class User(models.Model):
    name = models.CharField(max_length=32, null=True)
    email = models.CharField(max_length=64, unique=True)
    password = models.CharField(max_length=128, null=True)

    class Meta:
        db_table = "users"
