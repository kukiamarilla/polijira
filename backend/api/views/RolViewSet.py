from backend.api.serializers.PermisoSerializer import PermisoSerializer
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework import response
from rest_framework.response import Response
from backend.api.models import Rol, Permiso, Usuario
from backend.api.serializers import RolSerializer, PermisoSerializer
from django.db import transaction


class RolViewSet(viewsets.ViewSet):
    """
    RolViewSet View para el modelo Rol

    Args:
        viewsets (module): tipo de clase basado en view
    """

    def list(self, request):
        """
        list Lista todos los roles de sistema

        Args:
            request (Any): request

        Return:
            json: lista de roles de sistema en formato json
        """
        usuario_request = Usuario.objects.get(user=request.user)
        if not usuario_request.tiene_permiso("ver_roles"):
            response = {
                "message": "No tiene permiso para realizar esta acción",
                "permission_required": ["ver_roles"]
            }
            return Response(response, status=status.HTTP_403_FORBIDDEN)
        roles = Rol.objects.all()
        serializer = RolSerializer(roles, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        retrieve Obtiene un rol de sistema mediante su pk

        Args:
            request (Any): request
            pk (integer, opcional): primary key. Defaults to None.

        Returns:
            json: rol de sistema obtenido en formato json
        """
        try:
            usuario_request = Usuario.objects.get(user=request.user)
            if not usuario_request.tiene_permiso("ver_roles"):
                response = {
                    "message": "No tiene permiso para realizar esta acción",
                    "permission_required": ["ver_roles"]
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            rol = Rol.objects.get(pk=pk)
            serializer = RolSerializer(rol, many=False)
            return Response(serializer.data)
        except Rol.DoesNotExist:
            response = {"message": "No existe el rol"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)

    @transaction.atomic
    def create(self, request):
        """
        create Crea un rol de sistema

        Args:
            request (Any): request

        Returns:
            json: rol de sistema creado en formato json
        """
        try:
            usuario_request = Usuario.objects.get(user=request.user)
            if not (usuario_request.tiene_permiso("crear_roles") and usuario_request.tiene_permiso("ver_permisos")):
                response = {
                    "message": "No tiene permiso para realizar esta acción",
                    "permission_required": [
                        "ver_permisos",
                        "crear_roles"
                    ]
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            permisos = request.data["permisos"]
            if len(permisos) == 0:
                response = {"message": "Debe tener al menos un permiso"}
                return Response(response, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            rol = Rol.objects.create(nombre=request.data["nombre"])
            for p in permisos:
                perm = Permiso.objects.get(pk=p["id"])
                rol.agregar_permiso(perm)
            serializer = RolSerializer(rol, many=False)
            return Response(serializer.data)
        except Permiso.DoesNotExist:
            transaction.set_rollback(True)
            response = {"message": "No existe el permiso"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        """
        destroy Elimina un rol de sistema

        Args:
            request (Any): request
            pk (integer, opcional): primary key. Defaults to None.
        """
        try:
            usuario_request = Usuario.objects.get(user=request.user)
            if not (usuario_request.tiene_permiso("ver_roles") and usuario_request.tiene_permiso("eliminar_roles")):
                response = {
                    "message": "No tiene permiso para realizar esta acción",
                    "permission_required": [
                        "ver_roles",
                        "eliminar_roles"
                    ]
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            rol = Rol.objects.get(pk=pk)
            rol.delete()
            response = {"message": "Rol Eliminado."}
            return Response(response)
        except Rol.DoesNotExist:
            response = {"message": "No existe el rol"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        """
        update Obtiene un rol de sistema mediante su pk

        Args:
            request (Any): request
            pk (integer, opcional): primary key. Defaults to None.

        Returns:
            json: rol de sistema modificado en formato json
        """
        try:
            usuario_request = Usuario.objects.get(user=request.user)
            if not (usuario_request.tiene_permiso("ver_permisos") and usuario_request.tiene_permiso("ver_roles") and usuario_request.tiene_permiso("modificar_roles")):
                response = {
                    "message": "No tiene permiso para realizar esta acción",
                    "permission_required": [
                        "ver_permisos",
                        "ver_roles",
                        "modificar_roles"
                    ]
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            rol = Rol.objects.get(pk=pk)
            rol.nombre = request.data["nombre"]
            rol.save()
            serializer = RolSerializer(rol, many=False)
            return Response(serializer.data)
        except Rol.DoesNotExist:
            response = {"message": "No existe el rol"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=["GET"])
    def permisos(self, request, pk=None):
        """
        permisos Lista los permisos de un rol de sistema

            request (Any): request
            pk (integer, opcional): primary key. Defaults to None.

        Returns:
            json: lista de permisos de un rol de sistema
        """
        try:
            usuario_request = Usuario.objects.get(user=request.user)
            if not usuario_request.tiene_permiso("ver_roles"):
                response = {
                    "message": "No tiene permiso para realizar esta acción",
                    "permission_required": ["ver_roles"]
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            rol = Rol.objects.get(pk=pk)
            permisos = rol.permisos.all()
            serializer = PermisoSerializer(permisos, many=True)
            return Response(serializer.data)
        except Rol.DoesNotExist:
            response = {"message": "No existe el rol"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)

    @permisos.mapping.post
    def agregar_permiso(self, request, pk=None):
        """
        agregar_permiso Agrega un permiso a un rol de sistema

        Args:
            request (Any): request
            pk (integer, opcional): primary key. Defaults to None.

        Returns:
            json: rol de sistema con nuevo permiso agregado en formato json
        """
        try:
            usuario_request = Usuario.objects.get(user=request.user)
            if not (usuario_request.tiene_permiso("ver_permisos") and usuario_request.tiene_permiso("modificar_roles")):
                response = {
                    "message": "No tiene permiso para realizar esta acción",
                    "permission_required": [
                        "ver_permisos",
                        "modificar_roles"
                    ]
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            rol = Rol.objects.get(pk=pk)
            permiso = Permiso.objects.get(pk=request.data["permiso_id"])
            rol.agregar_permiso(permiso)
            serializer = RolSerializer(rol, many=False)
            return Response(serializer.data)
        except Permiso.DoesNotExist:
            response = {"message": "No existe el permiso"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Rol.DoesNotExist:
            response = {"message": "No existe el rol"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)

    @permisos.mapping.delete
    def eliminar_permiso(self, request, pk=None):
        """
        eliminar_permiso Elimina un permiso de un rol de sistema

        Args:
            request (Any): request
            pk (integer, opcional): primary key. Defaults to None.
        """
        try:
            usuario_request = Usuario.objects.get(user=request.user)
            if not (usuario_request.tiene_permiso("ver_permisos") and usuario_request.tiene_permiso("modificar_roles")):
                response = {
                    "message": "No tiene permiso para realizar esta acción",
                    "permission_required": [
                        "ver_permisos",
                        "modificar_roles"
                    ]
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            rol = Rol.objects.get(pk=pk)
            permiso = Permiso.objects.get(pk=request.data["permiso_id"])
            rol.eliminar_permiso(permiso)
            serializer = RolSerializer(rol, many=False)
            return Response(serializer.data)
        except Permiso.DoesNotExist:
            response = {"message": "No existe el permiso"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Rol.DoesNotExist:
            response = {"message": "No existe el rol"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)
