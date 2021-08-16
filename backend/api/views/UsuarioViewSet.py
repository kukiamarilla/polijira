from rest_framework import viewsets
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
