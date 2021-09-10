from rest_framework import serializers
from backend.api.models import RolProyecto
from backend.api.serializers import ProyectoSerializer, PermisoProyectoSerializer


class RolProyectoSerializer(serializers.ModelSerializer):
    """
    Serializer de Rol de Proyecto
    """
    permisos = PermisoProyectoSerializer(many=True, read_only=True)
    proyecto = ProyectoSerializer(many=False, read_only=True)

    class Meta:
        """
         Metadatos de RolProyectoSerializer
        """
        model = RolProyecto
        fields = ("id", "nombre", "permisos", "proyecto")
