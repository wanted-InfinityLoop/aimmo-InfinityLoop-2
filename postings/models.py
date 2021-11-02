from django.db import models
from core.models import AbstractTimeStamped

class Category(models.Model):
    name = models.CharField(max_length=20)
    
    class Meta:
        db_table = "categories"

class Posting(AbstractTimeStamped):
    title    = models.CharField(max_length=128, default="")
    text     = models.TextField()
    author   = models.ForeignKey("users.User", on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, related_name = "posting")

    class Meta:
        db_table = "postings"