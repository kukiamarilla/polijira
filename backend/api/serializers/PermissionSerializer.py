from rest_framework import serializers
from django.contrib.auth.models import Permission


class PermissionSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Permission
    """

    class Meta:
        """
         Metadatos del Permission Serializer
        """
        model = Permission
        fields = ("codename", "name", "content_type")
