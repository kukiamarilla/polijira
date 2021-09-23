from rest_framework import serializers
from backend.api.models import UserStory


class UserStorySerializer(serializers.ModelSerializer):
    """
    UserStorySerializer Serializer para el modelo User Story

    Args:
        serializers (ModelSerializer): Serializer del módulo rest_framework
    """

    class Meta:
        """
         Metadatos del modelo User Story
        """
        model = UserStory
        fields = (
            "id",
            "nombre",
            "descripcion",
            "estado",
            "fecha_release",
            "fecha_creacion",
            "desarrollador",
            "estado_estimacion",
            "product_backlog"
        )
