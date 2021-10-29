from rest_framework import serializers
from backend.api.models import Actividad


class ActividadSerializer(serializers.ModelSerializer):
    """
    ActividadSerializer Serializer del modelo Actividad

    Args:
        serializers (ModelSerializer): Serializer del módulo Rest Framework
    """

    class Meta:
        """
         Metadatos de Actividad
        """
        model = Actividad
        fields = (
            "id",
            "descripcion",
            "horas",
            "fecha_creacion",
            "user_story"
        )
