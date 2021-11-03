from .models import User
from rest_framework import serializers


class UserSignInSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password"]


class UserSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["name", "email", "password"]
