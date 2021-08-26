from django.db.models.base import ModelStateFieldsCacheDescriptor
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from backend.api.models import Usuario
from backend.api.models import Rol
from backend.api.serializers import UsuarioSerializer


class UsuarioViewSet(viewsets.ViewSet):
    """
    UsuarioViewSet View para el modelo Usuario

    Args:
        viewsets (module): tipo de clase basado en view

    """
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
            serializer = UsuarioSerializer(usuario, many=False)
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
        except Usuario.DoesNotExist:
            response = {"message": "No existe el usuario"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['POST'])
    def desactivar(self, request, pk=None):
        """
        desactivar Desactiva el usuario con la pk especificada

        Args:
            request (Any): request
            pk (integer, opcional): primary key. Defaults to None.

        Returns:
            json: usuario desactivado en formato json
        """
        try:
            # Falta incluir permisos
            usuario = Usuario.objects.get(pk=pk)
            if request.user == usuario.user:
                response = {"message": "No puedes desactivarte a ti mismo"}
                return Response(response, status=status.HTTP_409_CONFLICT)
            usuario.desactivar()
            serializer = UsuarioSerializer(usuario, many=False)
            return Response(serializer.data)
        except Usuario.DoesNotExist:
            response = {"message": "No existe el usuario"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['POST'])
    def asignar_rol(self, request, pk=None):
        try:
            usuario = Usuario.objects.get(pk=pk)
            if not usuario.tiene_permiso("asignar_roles"):
                response = {"message": "Debe tener permiso para asignar roles"}
                return Response(response, status=status.HTTP_401_UNAUTHORIZED)
            rol = Rol.objects.get(pk=request.data['id'])
            usuario.asignar_rol(rol)
        except Usuario.DoesNotExist:
            response = {"message": "No existe el usuario"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Rol.DoesNotExist:
            response = {"message": "No existe el rol"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)
