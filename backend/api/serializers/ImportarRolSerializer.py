from rest_framework import serializers
from backend.api.models import Proyecto
from backend.api.serializers import RolProyectoSerializer


class ImportarRolSerializer(serializers.ModelSerializer):
    """
    Serializer de Importar Rol
    """
    roles = RolProyectoSerializer(many=True, read_only=True)

    class Meta:
        """
         Metadatos de ImportarRolSerializer
        """
        model = Proyecto
        fields = ("id", "nombre", "roles")
