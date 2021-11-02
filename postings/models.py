from django.db import models


class Posting(models.Model):
    title = models.CharField(max_length=128, default="")
    text = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey("users.User", on_delete=models.CASCADE)

    class Meta:
        db_table = "postings"
