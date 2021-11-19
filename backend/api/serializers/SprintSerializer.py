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
            "fecha_fin_real",
            "estado",
            "estado_sprint_planning",
            "planificador",
            "proyecto"
        )
