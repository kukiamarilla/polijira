from rest_framework import viewsets, status
from rest_framework.response import Response
from backend.api.models import PermisoProyecto, Usuario
from backend.api.serializers import PermisoProyectoSerializer


class PermisoProyectoViewSet(viewsets.ViewSet):
    """
    PermisoProyectoViewSet View para el modelo PermisoProyecto

    Args:
        viewsets (module): tipo de clase basado en view
    """

    def list(self, request):
        """
        list Lista todos los permisos de proyecto
        Args:
            request (Any): request
        Return:
            JSON: List(PermisoProyecto)
        """
        usuario_request = Usuario.objects.get(user=request.user)
        if not usuario_request.tiene_PermisoProyecto("ver_permisos"):
            response = {
                "message": "No tiene permiso para realizar esta acción",
                "permission_required": ["ver_permisos"]
            }
            return Response(response, status=status.HTTP_403_FORBIDDEN)
        permisos = PermisoProyecto.objects.all()
        serializer = PermisoProyectoSerializer(permisos, many=True)
        return Response(serializer.data)
