from rest_framework import serializers
from backend.api.models import PlantillaRolProyecto
from .PermisoProyectoSerializer import PermisoProyectoSerializer


class PlantillaRolProyectoSerializer(serializers.ModelSerializer):
    """
    Serializer de PlantillaRolProyecto
    """
    permisos = PermisoProyectoSerializer(many=True, read_only=True)

    class Meta:
        """
         Metadatos de PlantillaRolProyectoSerializer
        """
        model = PlantillaRolProyecto
        fields = ("id", "nombre", "permisos")
