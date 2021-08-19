from rest_framework import serializers
from backend.api.models import Permiso
from backend.api.serializers import PermissionSerializer


class PermisoSerializer(serializers.ModelSerializer):
    """
    Serializer de Permiso
    """
    permission = PermissionSerializer(many=False, read_only=True)

    class Meta:
        """
         Metadatos de PermisoSerializer
        """
        model = Permiso
        fields = ("id", "nombre", "codigo", "permission")
