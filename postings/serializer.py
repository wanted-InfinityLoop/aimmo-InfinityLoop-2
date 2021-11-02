from .models import Posting
from rest_framework import serializers


class PostingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posting
        fields = ["title", "text"]
