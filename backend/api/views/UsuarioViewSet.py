from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from backend.api.models import MiembroSprint, Usuario, Rol
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
        usuario_request = Usuario.objects.get(user=request.user)
        serializer = UsuarioSerializer(usuario_request, many=False)
        return Response(serializer.data)

    def list(self, request):
        """
        list Lista todos los usuarios del sistema

        Args:
            request (Any): request

        Returns:
            json: lista de usuarios en formato json
        """
        usuario_request = Usuario.objects.get(user=request.user)
        if not usuario_request.tiene_permiso("ver_usuarios"):
            response = {
                "message": "No tiene permiso para realizar esta acción",
                "permission_required": ["ver_usuarios"]
            }
            return Response(response, status=status.HTTP_403_FORBIDDEN)
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
            usuario_request = Usuario.objects.get(user=request.user)
            if not usuario_request.tiene_permiso("ver_usuarios"):
                response = {
                    "message": "No tiene permiso para realizar esta acción",
                    "permission_required": ["ver_usuarios"]
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
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
            usuario_request = Usuario.objects.get(user=request.user)
            if not usuario_request.tiene_permiso("activar_usuarios"):
                response = {
                    "message": "No tiene permiso para realizar esta acción",
                    "permission_required": ["activar_usuarios"]
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            usuario = Usuario.objects.get(pk=pk)
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
            usuario_request = Usuario.objects.get(user=request.user)
            if not usuario_request.tiene_permiso("desactivar_usuarios"):
                response = {
                    "message": "No tiene permiso para realizar esta acción",
                    "permission_required": ["desactivar_usuarios"]
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            usuario = Usuario.objects.get(pk=pk)
            if usuario_request == usuario:
                response = {"message": "No puedes desactivarte a ti mismo"}
                return Response(response, status=status.HTTP_409_CONFLICT)
            if MiembroSprint.pertenece_a_sprint_activo(usuario):
                response = {
                    "message": "Este usuario pertenece a un Sprint Activo",
                    "error": "conflict"
                }
                return Response(response, status=status.HTTP_409_CONFLICT)
            usuario.desactivar()
            serializer = UsuarioSerializer(usuario, many=False)
            return Response(serializer.data)
        except Usuario.DoesNotExist:
            response = {"message": "No existe el usuario"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['POST'])
    def asignar_rol(self, request, pk=None):
        """
        asignar_rol Asigna un rol a un usuario

        Args:
            request (Any): request
            pk (int, opcional): primary key. Defaults to None.

        Returns:
            json: html response
        """
        try:
            usuario_request = Usuario.objects.get(user=request.user)
            usuario = Usuario.objects.get(pk=pk)
            if not (usuario_request.tiene_permiso("ver_usuarios") and usuario_request.tiene_permiso("ver_roles")
                    and usuario_request.tiene_permiso("asignar_roles")):
                response = {
                    "message": "No tiene permiso para realizar esta acción",
                    "permission_required": [
                        "ver_usuarios",
                        "ver_roles",
                        "asignar_roles"
                    ]
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            if usuario_request == usuario:
                response = {"message": "No puede asignarse roles a sí mismo"}
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            rol = Rol.objects.get(pk=request.data['id'])
            usuario.asignar_rol(rol)
            serializer = UsuarioSerializer(usuario, many=False)
            return Response(serializer.data)
        except Usuario.DoesNotExist:
            response = {"message": "No existe el usuario"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Rol.DoesNotExist:
            response = {"message": "No existe el rol"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)
