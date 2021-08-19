from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo User
    """

    class Meta:
        """
         Metadatos del User Serializer
        """
        model = User
        fields = ("username", "first_name", "last_name", "email")
