from rest_framework import serializers
from backend.api.models import Actividad
from backend.api.serializers.UsuarioSerializer import UsuarioSerializer


class ActividadSerializer(serializers.ModelSerializer):
    """
    ActividadSerializer Serializer del modelo Actividad

    Args:
        serializers (ModelSerializer): Serializer del módulo Rest Framework
    """

    desarrollador = UsuarioSerializer(many=False, read_only=True)

    class Meta:
        """
         Metadatos de Actividad
        """
        model = Actividad
        fields = (
            "id",
            "titulo",
            "descripcion",
            "horas",
            "fecha_creacion",
            "sprint_backlog",
            "desarrollador",
        )
