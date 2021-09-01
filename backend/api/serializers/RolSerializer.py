from rest_framework import serializers
from backend.api.models import Rol
from .PermisoSerializer import PermisoSerializer


class RolSerializer(serializers.ModelSerializer):
    """
    Serializer de Rol
    """
    permisos = PermisoSerializer(many=True, read_only=True)

    class Meta:
        """
         Metadatos de RolSerializer
        """
        model = Rol
        fields = ("id", "nombre", "permisos")
