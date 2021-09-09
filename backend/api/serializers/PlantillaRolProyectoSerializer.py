from rest_framework import serializers
from backend.api.models import PlantillaRolProyecto
from .PermisoSerializer import PermisoSerializer


class PlantillaRolProyectoSerializer(serializers.ModelSerializer):
    """
    Serializer de PlantillaRolProyecto
    """
    permisos = PermisoSerializer(many=True, read_only=True)

    class Meta:
        """
         Metadatos de PlantillaRolProyectoSerializer
        """
        model = PlantillaRolProyecto
        fields = ("id", "nombre", "permisos")
