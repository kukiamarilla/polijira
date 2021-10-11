from rest_framework import serializers
from backend.api.models import MiembroSprint


class MiembroSprintSerializer(serializers.ModelSerializer):
    """
    Serializer de MiembroSprint

    Args:
        serializers (ModelSerializer): Serializer del módulo rest_framework
    """

    class Meta:
        """
        Metadatos de MiembroSprintSerializer

        """
        model = MiembroSprint
        fields = ("id", "miembro_proyecto", "sprint")
