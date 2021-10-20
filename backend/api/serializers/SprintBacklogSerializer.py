from rest_framework import serializers
from backend.api.models import SprintBacklog
from backend.api.serializers import SprintSerializer, UserStorySerializer


class SprintBacklogSerializer(serializers.ModelSerializer):
    """
    SprintBacklogSerializer Serializer para el modelo Sprint Backlog

    Args:
        serializers (ModelSerializer): Modelo Serializer del módulo rest framework
    """
    sprint = SprintSerializer(many=False, read_only=True)
    user_story = UserStorySerializer(many=False, read_only=True)

    class Meta:
        """
         Metadatos de Sprint Backlog
        """
        model = SprintBacklog
        fields = ("sprint", "user_story", "estado_kanban")
