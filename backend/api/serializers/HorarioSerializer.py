from backend.api.models import Horario
from rest_framework import serializers


class HorarioSerializer(serializers.ModelSerializer):
    """
    HorarioSerializer Serializer de Horario

    Args:
        serializers (ModelSerializer): Serializer del modulo rest_framework
    """

    class Meta:
        """
         Metadatos de Horario
        """
        model = Horario
        fields = (
            "id",
            "lunes",
            "martes",
            "miercoles",
            "jueves",
            "viernes",
            "sabado",
            "domingo"
        )
