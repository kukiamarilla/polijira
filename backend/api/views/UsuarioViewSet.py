from rest_framework import viewsets, status
from rest_framework import response
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

    def retrieve(self, request, pk=None):
        """
        retrieve Obtiene un usuario mediante su pk

        Args:
            request (Any): request
            pk (integer, opcional): primary key. Defaults to None.

        Returns:
            json: usuario obtenido en formato json
        """
        try:
            usuario = Usuario.objects.get(pk=pk)
            serializer = UsuarioSerializer(usuario[0], many=False)
            return Response(serializer.data)
        except Usuario.DoesNotExist:
            response = {"message": "No existe el usuario"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['POST'])
    def activar(self, request, pk=None):
        """
        activar Activa el usuario con la pk especificada

        Args:
            request (Any): request
            pk (integer, opcional): primary key. Defaults to None.

        Returns:
            json: usuario activado en formato json 
        """
        try:
            usuario = Usuario.objects.get(pk=pk)
            # Falta incluir permisos
            usuario.activar()
            serializer = UsuarioSerializer(usuario, many=False)
            return Response(serializer.data)
        except Exception:
            response = {"message": "No existe el usuario"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['POST'])
    def desactivar(self, request, pk=None):

        try:
            usuario = Usuario.objects.get(pk=pk)
            # Falta incluir permisos
            usuario.desactivar()
            serializer = UsuarioSerializer(usuario, many=False)
            return Response(serializer.data)
        except Usuario.DoesNotExist:
            response = {"message": "No existe el usuario"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)
