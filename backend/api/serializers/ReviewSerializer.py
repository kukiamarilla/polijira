from rest_framework import serializers
from backend.api.models import Review
from backend.api.serializers import UsuarioSerializer


class ReviewSerializer(serializers.ModelSerializer):
    """
    ReviewSerializer Serializer para el modelo Review

    Args:
        serializers (ModelSerializer): Serializer del módulo rest_framework
    """

    autor = UsuarioSerializer(many=False, read_only=True)

    class Meta:
        """
         Metadatos del Review Serializer
        """
        model = Review
        fields = ("id", "user_story", "observacion", "fecha_creacion", "autor")
