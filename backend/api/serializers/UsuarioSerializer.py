from rest_framework import serializers
from backend.api.models import Usuario
from .UserSerializer import UserSerializer
from .RolSerializer import RolSerializer


class UsuarioSerializer(serializers.ModelSerializer):
    """
    Serializer de Usuarios
    """
    user = UserSerializer(many=False, read_only=True)
    rol = RolSerializer(many=False, read_only=True)

    class Meta:
        """
         Metadatos de UsuarioSerializer
        """
        model = Usuario
        fields = ("id", "nombre", "email", "estado", "firebase_uid", "user", "rol")
