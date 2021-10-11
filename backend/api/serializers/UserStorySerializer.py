from rest_framework import serializers
from backend.api.models import UserStory
from backend.api.serializers import MiembroSerializer
from backend.api.serializers import RegistroUserStorySerializer


class UserStorySerializer(serializers.ModelSerializer):
    """
    UserStorySerializer Serializer para el modelo User Story

    Args:
        serializers (ModelSerializer): Serializer del módulo rest_framework
    """
<<<<<<< HEAD
=======
    desarrollador = MiembroSerializer(many=False, read_only=True)
    registros = RegistroUserStorySerializer(many=True, read_only=True)
>>>>>>> develop

    class Meta:
        """
         Metadatos del modelo User Story
        """
        model = UserStory
        fields = (
            "id",
            "nombre",
            "descripcion",
            "horas_estimadas",
            "prioridad",
            "estado",
            "fecha_release",
            "fecha_creacion",
            "desarrollador",
            "estado_estimacion",
            "product_backlog",
            "registros"
        )
