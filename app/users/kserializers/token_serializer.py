
#serializer.py
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .user_serializer import UserSerializer

class MyCustomTokenSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(source="user.id")

    class Meta:
        model = Token
        fields = ('key', 'user')