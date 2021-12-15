from .models        import Comment, Posting
from rest_framework import serializers


class PostingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posting
        fields = ["title", "text", "category"]

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["content"]

