from rest_framework import serializers
from backend.api.models import MiembroSprint
from backend.api.serializers import MiembroSerializer


class MiembroSprintSerializer(serializers.ModelSerializer):
    """
    Serializer de MiembroSprint

    Args:
        serializers (ModelSerializer): Serializer del módulo rest_framework
    """

    miembro_proyecto = MiembroSerializer(read_only=True, many=False)

    class Meta:
        """
        Metadatos de MiembroSprintSerializer

        """
        model = MiembroSprint
        fields = ("id", "miembro_proyecto", "sprint")
