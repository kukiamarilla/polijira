from django.db import transaction
from backend.api.decorators import FormValidator
from rest_framework.decorators import action
from backend.api.serializers import RolProyectoSerializer, PermisoProyectoSerializer
from backend.api.models import Proyecto, RolProyecto, PermisoProyecto, Usuario
from rest_framework import viewsets, status
from rest_framework.response import Response
from backend.api.forms import \
    CreateRolProyectoForm, \
    UpdateRolProyectoForm, \
    AgregarPermisoRolProyectoForm


class RolProyectoViewSet(viewsets.ViewSet):
    """
    RolProyectoViewSet View para RolProyecto

    Args:
        views (ViewSet): Tipo de clase basado en View
    """

    def list(self, request):
        """
        list Lista todos los roles de proyecto

        Args:
            request (Any): request

        Return:
            JSON: Roles de proyecto
        """
        # ACA TRAER MIEMBRO DE USUARIO
        # usuario_request = Usuario.objects.get(user=request.user)
        # if not usuario_request.tiene_permiso("ver_roles_proyecto"):
        #     response = {_proyecto
        #         "message": "No tiene permiso para realizar esta acción",
        #         "permission_required": ["ver_roles_proyecto"]
        #     }
        #     return Response(response, status=status.HTTP_403_FORBIDDEN)
        roles = RolProyecto.objects.all()
        serializer = RolProyectoSerializer(roles, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        retrieve Obtiene un rol de proyecto

        Args:
            request (Any): request
            pk (integer, opcional): Primary Key

        Returns:
            JSON: un rol de proyecto
        """
        try:
            # ACA TRAER MIEMBRO
            # usuario_request = Usuario.objects.get(user=request.user)
            # if not usuario_request.tiene_permiso("ver_roles_proyecto") or \
            #    not usuario_request.tiene_permiso("ver_permisos_proyecto"):
            #     response = {
            #         "message": "No tiene permiso para realizar esta acción",
            #         "permission_required": ["ver_roles_proyecto", "ver_permisos_proyecto"]
            #     }
            #     return Response(response, status=status.HTTP_403_FORBIDDEN)
            rol = RolProyecto.objects.get(pk=pk)
            serializer = RolProyectoSerializer(rol, many=False)
            return Response(serializer.data)
        except RolProyecto.DoesNotExist:
            response = {"message": "No existe el rol de proyecto"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)

    @transaction.atomic
    @FormValidator(form=CreateRolProyectoForm)
    def create(self, request):
        """
        create Crea un rol de proyecto

        Args:
            request (Any): request

        Returns:
            JSON: Rol de proyecto
        """
        try:
            # ACA TRAER MIEMBRO
            # usuario_request = Usuario.objects.get(user=request.user)
            # if not usuario_request.tiene_permiso("crear_roles_proyecto") or \
            #    not usuario_request.tiene_permiso("ver_permisos_proyecto"):
            #     response = {
            #         "message": "No tiene permiso para realizar esta acción",
            #         "permission_required": [
            #             "ver_permisos_proyecto",
            #             "crear_roles_proyecto"
            #         ]
            #     }
            #     return Response(response, status=status.HTTP_403_FORBIDDEN)
            permisos = request.data["permisos"]
            proyecto = Proyecto.objects.get(pk=request.data["proyecto"])
            rol = RolProyecto.objects.create(nombre=request.data["nombre"], proyecto=proyecto)
            for p in permisos:
                perm = PermisoProyecto.objects.get(pk=p["id"])
                rol.agregar_permiso(perm)
            serializer = RolProyectoSerializer(rol, many=False)
            return Response(serializer.data)
        except Proyecto.DoesNotExist:
            response = {"message": "No existe el proyecto"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        """
        destroy Elimina un rol de proyecto

        Args:
            request (Any): request
            pk (integer, opcional): Primary Key
        """
        try:
            # ACA MIEMBRO
            # usuario_request = Usuario.objects.get(user=request.user)
            # if not (usuario_request.tiene_permiso("ver_roles_proyecto") and usuario_request.tiene_permiso("eliminar_roles_proyecto")):
            #     response = {
            #         "message": "No tiene permiso para realizar esta acción",
            #         "permission_required": [
            #             "ver_roles_proyecto",
            #             "eliminar_roles_proyecto"
            #         ]
            #     }
            #     return Response(response, status=status.HTTP_403_FORBIDDEN)
            # SI UN MIEMBRO ESTA ASIGNADO A ESE ROL,
            #  if RolProyecto.objects.filter(rol__pk=pk).count():
            #     response = {"message": "Rol asignado a un miembro de proyecto, no se puede eliminar"}
            #     return Response(response, status=status.HTTP_403_FORBIDDEN)
            rol = RolProyecto.objects.get(pk=pk)
            rol.delete()
            response = {"message": "Rol de Proyecto Eliminado."}
            return Response(response)
        except RolProyecto.DoesNotExist:
            response = {"message": "No existe el rol de proyecto"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)

    @FormValidator(UpdateRolProyectoForm)
    def update(self, request, pk=None):
        """
        update Obtiene un rol de proyecto mediante su pk

        Args:
            request (Any): request
            pk (integer, opcional): Primary Key

        Returns:
            JSON: rol de proyecto modificado en formato json
        """
        try:
            # ACA MIEMBRO
            # usuario_request = Usuario.objects.get(user=request.user)
            # if not usuario_request.tiene_permiso("ver_permisos_proyecto") or \
            #    not usuario_request.tiene_permiso("ver_roles_proyecto") or \
            #    not usuario_request.tiene_permiso("modificar_roles_proyecto"):
            #     response = {
            #         "message": "No tiene permiso para realizar esta acción",
            #         "permission_required": [
            #             "ver_permisos_proyecto",
            #             "ver_roles_proyecto",
            #             "modificar_roles_proyecto"
            #         ]
            #     }
            #     return Response(response, status=status.HTTP_403_FORBIDDEN)
            # SI ES EL ROL DEL MIEMBRO
            # if (usuario_request.rol.pk == int(pk)):
            #     response = {"message": "No puedes modificar tu propio rol"}
            #     return Response(response, status=status.HTTP_403_FORBIDDEN)
            rol = RolProyecto.objects.get(pk=pk)
            rol.nombre = request.data["nombre"]
            rol.save()
            serializer = RolProyectoSerializer(rol, many=False)
            return Response(serializer.data)
        except RolProyecto.DoesNotExist:
            response = {"message": "No existe el rol de proyecto"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=["GET"])
    def permisos(self, request, pk=None):
        """
        permisos Lista los permisos de un rol de proyecto

            request (Any): request
            pk (integer, opcional): Primary Key

        Returns:
            JSON: lista de permisos del rol de proyecto con la pk especificada
        """
        try:
            # ACA MIEMBRO
            # usuario_request = Usuario.objects.get(user=request.user)
            # if not usuario_request.tiene_permiso("ver_roles_proyecto"):
            #     response = {
            #         "message": "No tiene permiso para realizar esta acción",
            #         "permission_required": ["ver_roles_proyecto"]
            #     }
            #     return Response(response, status=status.HTTP_403_FORBIDDEN)
            rol = RolProyecto.objects.get(pk=pk)
            permisos = rol.permisos.all()
            serializer = PermisoProyectoSerializer(permisos, many=True)
            return Response(serializer.data)
        except RolProyecto.DoesNotExist:
            response = {"message": "No existe el rol de proyecto"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)

    @permisos.mapping.post
    def agregar_permiso(self, request, pk=None):
        """
        agregar_permiso Agrega un permiso a un rol de proyecto

        Args:
            request (Any): request
            pk (integer, opcional): Primary Key

        Returns:
            JSON: Rol de proyecto con nuevo permiso agregado en formato json
        """
        try:
            # ACA MIEMBRO
            # usuario_request = Usuario.objects.get(user=request.user)
            # if not (usuario_request.tiene_permiso("ver_permisos_proyecto")
            #         and usuario_request.tiene_permiso("modificar_roles_proyecto")):
            #     response = {
            #         "message": "No tiene permiso para realizar esta acción",
            #         "permission_required": [
            #             "ver_permisos_proyecto",
            #             "modificar_roles_proyecto"
            #         ]
            #     }
            #     return Response(response, status=status.HTTP_403_FORBIDDEN)
            form = AgregarPermisoRolProyectoForm(request.data)
            if not form.is_valid():
                response = {
                    "message": "Error de validacion",
                    "errors": form.errors
                }
                return Response(response, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            # SI ES ROL DE MIEMBRO
            # if (usuario_request.rol.pk == int(pk)):
            #     response = {"message": "No puedes modificar tu propio rol"}
            #     return Response(response, status=status.HTTP_403_FORBIDDEN)
            rol = RolProyecto.objects.get(pk=pk)
            permiso = PermisoProyecto.objects.get(pk=request.data["id"])
            rol.agregar_permiso(permiso)
            serializer = RolProyectoSerializer(rol, many=False)
            return Response(serializer.data)
        except RolProyecto.DoesNotExist:
            response = {"message": "No existe el rol de proyecto"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)

    @permisos.mapping.delete
    def eliminar_permiso(self, request, pk=None):
        """
        eliminar_permiso Elimina un permiso de un rol de proyecto

        Args:
            request (Any): request
            pk (integer, opcional): Primary Key
        """
        try:
            # ACA MIEMBRO
            # usuario_request = Usuario.objects.get(user=request.user)
            # if not (usuario_request.tiene_permiso("ver_permisos_proyecto")
            #         and usuario_request.tiene_permiso("modificar_roles_proyecto")):
            #     response = {
            #         "message": "No tiene permiso para realizar esta acción",
            #         "permission_required": [
            #             "ver_permisos_proyecto",
            #             "modificar_roles_proyecto"
            #         ]
            #     }
            #     return Response(response, status=status.HTTP_403_FORBIDDEN)
            # SI ES ROL DEL MIEMBRO
            # if (usuario_request.rol.pk == int(pk)):
            #     response = {"message": "No puedes modificar tu propio rol"}
            #     return Response(response, status=status.HTTP_403_FORBIDDEN)
            rol = RolProyecto.objects.get(pk=pk)
            permiso = PermisoProyecto.objects.get(pk=request.data["id"])
            if rol.permisos.all().count() < 2:
                response = {"message": "El rol de proyecto no se puede quedar sin permisos"}
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            rol.eliminar_permiso(permiso)
            serializer = RolProyectoSerializer(rol, many=False)
            return Response(serializer.data)
        except PermisoProyecto.DoesNotExist:
            response = {"message": "No existe el permiso de proyecto"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except RolProyecto.DoesNotExist:
            response = {"message": "No existe el rol de proyecto"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)
