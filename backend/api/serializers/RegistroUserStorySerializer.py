from rest_framework import serializers
from backend.api.models import RegistroUserStory
from backend.api.serializers import MiembroSerializer


class RegistroUserStorySerializer(serializers.ModelSerializer):
    """
    RegistroUserStorySerializer Serializer para el modelo Registro de User Stories

    Args:
        serializers (ModelSerializer): Serializer del módulo rest_framework
    """
    autor = MiembroSerializer(many=False, read_only=True)

    class Meta:
        """
         Metadatos de Registro de User Stories
        """
        model = RegistroUserStory
        fields = (
            "id",
            "nombre_antes",
            "descripcion_antes",
            "prioridad_antes",
            "estado_antes",
            "nombre_despues",
            "descripcion_despues",
            "prioridad_despues",
            "estado_despues",
            "user_story",
            "accion",
            "autor",
            "fecha"
        )
