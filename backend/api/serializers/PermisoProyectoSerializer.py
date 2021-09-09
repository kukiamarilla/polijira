from rest_framework import serializers
from backend.api.models import PermisoProyecto


class PermisoProyectoSerializer(serializers.ModelSerializer):
    """
    Serializer de PermisoProyecto
    """

    class Meta:
        """
         Metadatos de PermisoProyectoSerializer
        """
        model = PermisoProyecto
        fields = ("id", "nombre", "codigo")
