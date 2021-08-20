from rest_framework import viewsets
from rest_framework.response import Response
from backend.api.models import Permiso
from backend.api.serializers import PermisoSerializer


class PermisoViewSet(viewsets.ViewSet):
    """
    PermisoViewSet [summary]

    Args:
        viewsets ([type]): [description]
    """

    def list(self, request):
        """
        list [summary]

        Args:
            request ([type]): [description]
        """
        permisos = Permiso.objects.all()
        serializer = PermisoSerializer(permisos, many=True)
        return Response(serializer.data)
