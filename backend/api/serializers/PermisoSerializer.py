from rest_framework import serializers
from backend.api.models import Permiso


class PermisoSerializer(serializers.ModelSerializer):
    """
    Serializer de Permiso
    """

    class Meta:
        """
         Metadatos de PermisoSerializer
        """
        model = Permiso
        fields = ("id", "nombre", "codigo")
