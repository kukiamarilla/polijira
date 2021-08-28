from rest_framework import viewsets
from rest_framework.response import Response
from backend.api.models import Permiso
from backend.api.serializers import PermisoSerializer


class PermisoViewSet(viewsets.ViewSet):
    """
    PermisoViewSet View para el modelo Permiso

    Args:
        viewsets (module): tipo de clase basado en view
    """

    def list(self, request):
        """
        list Lista todos los permisos del sistema
        Args:
            request (Any): Response
        Return:
            json: lista de permisos en formato json
        """
        # Falta el coso de validar si tiene permiso
        permisos = Permiso.objects.all()
        serializer = PermisoSerializer(permisos, many=True)
        return Response(serializer.data)
