from rest_framework import serializers
from backend.api.models import Usuario
from backend.api.serializers import UserSerializer


class UsuarioSerializer(serializers.ModelSerializer):
    """Serializer de User
    """
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Usuario
        fields = ("id", "nombre", "email", "estado", "firebase_uid")
