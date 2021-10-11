from rest_framework import serializers
from backend.api.models import RegistroUserStory


class RegistroUserStorySerializer(serializers.ModelSerializer):
    """
    RegistroUserStorySerializer Serializer para el modelo Registro de User Stories

    Args:
        serializers (ModelSerializer): Serializer del módulo rest_framework
    """
    class Meta:
        """
         Metadatos de Registro de User Stories
        """
        model = RegistroUserStory
        fields = (
            "id",
            "nombre_antes",
            "descripcion_antes",
            "horas_estimadas_antes",
            "prioridad_antes",
            "estado_antes",
            "desarrollador_antes",
            "nombre_despues",
            "descripcion_despues",
            "horas_estimadas_despues",
            "prioridad_despues",
            "estado_despues",
            "desarrollador_despues",
            "user_story",
            "accion",
            "autor",
            "fecha"
        )
