from rest_framework import serializers
from backend.api.models import UserStory
from backend.api.serializers import RegistroUserStorySerializer, ReviewSerializer


class UserStorySerializer(serializers.ModelSerializer):
    """
    UserStorySerializer Serializer para el modelo User Story

    Args:
        serializers (ModelSerializer): Serializer del módulo rest_framework
    """
    registros = RegistroUserStorySerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        """
         Metadatos del modelo User Story
        """
        model = UserStory
        fields = (
            "id",
            "nombre",
            "descripcion",
            "prioridad",
            "estado",
            "fecha_release",
            "fecha_creacion",
            "product_backlog",
            "reviews",
            "registros"
        )
