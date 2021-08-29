from rest_framework import viewsets, status
from rest_framework.response import Response
from backend.api.models import Permiso, Usuario
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
        usuario_request = Usuario.objects.get(user=request.user)
        if not usuario_request.tiene_permiso("ver_permisos"):
            response = {"message": "No tiene permisos para ver permisos"}
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)
        permisos = Permiso.objects.all()
        serializer = PermisoSerializer(permisos, many=True)
        return Response(serializer.data)
