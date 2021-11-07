from rest_framework import serializers
from backend.api.models import SprintBacklog
from backend.api.serializers import SprintSerializer, MiembroSprintSerializer, ActividadSerializer


class SprintBacklogSerializer(serializers.ModelSerializer):
    """
    SprintBacklogSerializer Serializer para el modelo Sprint Backlog

    Args:
        serializers (ModelSerializer): Modelo Serializer del módulo rest framework
    """
    sprint = SprintSerializer(many=False, read_only=True)
    desarrollador = MiembroSprintSerializer(many=False, read_only=True)
    actividades = ActividadSerializer(many=True, read_only=True)

    class Meta:
        """
         Metadatos de Sprint Backlog
        """
        model = SprintBacklog
        fields = (
            "id",
            "sprint",
            "user_story",
            "estado_kanban",
            "horas_estimadas",
            "estado_estimacion",
            "desarrollador",
            "actividades"
        )
