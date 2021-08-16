from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer de User de django
    """

    class Meta:
        models = User
        fields = ("username", "first_name", "last_name", "email")
