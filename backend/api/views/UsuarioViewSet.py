from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from backend.api.models import Usuario
from backend.api.serializers import UsuarioSerializer


class UsuarioViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['GET'])
    def me(self, request):
        """Obtiene el usuario autenticado

        Args:
            request (Any): request
        """
        user = request.user
        usuario = Usuario.objects.get(user=user)
        serializer = UsuarioSerializer(usuario, many=False)
        return Response(serializer.data)

    def list(self, request):
        """
        list Lista todos los usuarios del sistema

        Args:
            request (Any): request

        Returns:
            json: lista de usuarios en formato json
        """
        # Falta incluir permisos
        usuarios = Usuario.objects.all()
        serializer = UsuarioSerializer(usuarios, many=True)
        return Response(serializer.data)
