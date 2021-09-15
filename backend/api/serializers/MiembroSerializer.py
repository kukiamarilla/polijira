from rest_framework import serializers
from backend.api.models import Usuario
from .UsuarioSerializer import UsuarioSerializer
from .RolProyectoSerializer import RolProyectoSerializer
from .ProyectoSerializer import ProyectoSerializer


class MiembroSerializer(serializers.ModelSerializer):
    """
    Serializer de miembro
    """
    usuario = UsuarioSerializer(many=False, read_only=True)
    proyecto = ProyectoSerializer(many=False, read_only=True)
    rol = RolProyectoSerializer(many=False, read_only=True)

    class Meta:
        """
         Metadatos de MiembroSerializer
        """
        model = Usuario
        fields = ("id", "usuario", "proyecto", "rol")
