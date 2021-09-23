from rest_framework import serializers
from backend.api.models import UserStory


class UserStorySerializer(serializers.ModelSerializer):

    class Meta:
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
