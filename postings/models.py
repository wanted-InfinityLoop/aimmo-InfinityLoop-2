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
    count    = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "postings"

class Comment(models.Model):
    content        = models.CharField(max_length=500)
    user           = models.ForeignKey("users.User", on_delete=models.CASCADE)
    posting        = models.ForeignKey("Posting", on_delete=models.CASCADE)
    parent_comment = models.ForeignKey("self", on_delete=models.CASCADE, null=True)
    
    class Meta:
        db_table = 'comments'
