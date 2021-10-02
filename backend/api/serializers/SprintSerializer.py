from rest_framework import serializers
from backend.api.models import Sprint


class SprintSerializer(serializers.ModelSerializer):
    """
    SprintSerializer Serializer para el modelo Sprint

    Args:
        serializers (ModelSerializer): Serializer del módulo rest_framework
    """

    class Meta:
        """
         Metadatos del Sprint
        """
        model = Sprint
        fields = (
            "id",
            "numero",
            "fecha_inicio",
            "fecha_fin",
            "estado",
            "capacidad",
            "estado_sprint_backlog",
            "planificador"
        )
