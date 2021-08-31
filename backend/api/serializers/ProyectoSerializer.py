from backend.api.serializers import UsuarioSerializer
from rest_framework import serializers
from backend.api.models import Proyecto


class ProyectoSerializer(serializers.ModelSerializer):
    """
    ProyectoSerializer Serializer del modelo Proyecto
    """
    scrum_master = UsuarioSerializer(many=False, read_only=True)

    class Meta:
        """
         Metadatos de ProyectoSerializer
        """
        model = Proyecto
        fields = ('id', 'nombre', 'fecha_inicio', 'fecha_fin', 'estado', 'scrum_master')
