from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from backend.api.models import PlantillaRolProyecto, Permiso, Usuario
from backend.api.serializers import PlantillaRolProyectoSerializer, PermisoSerializer
from backend.api.decorators import FormValidator
from backend.api.forms import \
    AgregarPermisoRolForm, \
    CreatePlantillaRolProyectoForm, \
    UpdatePlantillaRolProyectoForm


class PlantillaRolProyectoViewSet(viewsets.ViewSet):
    """
    PlantillaRolProyectoViewSet View para PlantillaRolProyecto

    Args:
        viewsets (ViewSet): Tipo de clase basado en View
    """

    def list(self, request):
        """
        list Lista todos los roles de proyecto

        Args:
            request (Any): request

        Return:
            JSON: Roles de proyecto
        """
        usuario_request = Usuario.objects.get(user=request.user)
        if not usuario_request.tiene_permiso("ver_plantillas"):
            response = {
                "message": "No tiene permiso para realizar esta acción",
                "permission_required": ["ver_plantillas"]
            }
            return Response(response, status=status.HTTP_403_FORBIDDEN)
        roles = PlantillaRolProyecto.objects.all()
        serializer = PlantillaRolProyectoSerializer(roles, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        retrieve Obtiene una plantilla de rol de proyecto

        Args:
            request (Any): request
            pk (integer, opcional): Primary Key

        Returns:
            JSON: una plantilla de rol de proyecto
        """
        try:
            usuario_request = Usuario.objects.get(user=request.user)
            if not usuario_request.tiene_permiso("ver_plantillas") or \
               not usuario_request.tiene_permiso("ver_permisos"):
                response = {
                    "message": "No tiene permiso para realizar esta acción",
                    "permission_required": ["ver_plantillas", "ver_permisos"]
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            rol = PlantillaRolProyecto.objects.get(pk=pk)
            serializer = PlantillaRolProyectoSerializer(rol, many=False)
            return Response(serializer.data)
        except PlantillaRolProyecto.DoesNotExist:
            response = {"message": "No existe la plantilla de rol"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)

    @transaction.atomic
    @FormValidator(form=CreatePlantillaRolProyectoForm)
    def create(self, request):
        """
        create Crea una plantilla de rol de proyecto

        Args:
            request (Any): request

        Returns:
            JSON: Plantilla de rol de proyecto
        """

        usuario_request = Usuario.objects.get(user=request.user)
        if not usuario_request.tiene_permiso("crear_plantillas") or \
           not usuario_request.tiene_permiso("ver_permisos"):
            response = {
                "message": "No tiene permiso para realizar esta acción",
                "permission_required": [
                    "ver_permisos",
                    "crear_plantillas"
                ]
            }
            return Response(response, status=status.HTTP_403_FORBIDDEN)
        permisos = request.data["permisos"]
        rol = PlantillaRolProyecto.objects.create(nombre=request.data["nombre"])
        for p in permisos:
            perm = Permiso.objects.get(pk=p["id"])
            rol.agregar_permiso(perm)
        serializer = PlantillaRolProyectoSerializer(rol, many=False)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        """
        destroy Elimina una plantilla de rol de proyecto

        Args:
            request (Any): request
            pk (integer, opcional): Primary Key
        """
        try:
            usuario_request = Usuario.objects.get(user=request.user)
            if not (usuario_request.tiene_permiso("ver_plantillas") and usuario_request.tiene_permiso("eliminar_roles")):
                response = {
                    "message": "No tiene permiso para realizar esta acción",
                    "permission_required": [
                        "ver_plantillas",
                        "eliminar_roles"
                    ]
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            # if RolProyecto.objects.filter(rol__pk=pk).count():
            #     response = {"message": "Plantilla asignado a un rol, no se puede eliminar"}
            #     return Response(response, status=status.HTTP_403_FORBIDDEN)
            rol = PlantillaRolProyecto.objects.get(pk=pk)
            rol.delete()
            response = {"message": "Plantilla de rol Eliminado."}
            return Response(response)
        except PlantillaRolProyecto.DoesNotExist:
            response = {"message": "No existe la plantilla de rol"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)

    @FormValidator(UpdatePlantillaRolProyectoForm)
    def update(self, request, pk=None):
        """
        update Obtiene una plantilla de rol de proyecto

        Args:
            request (Any): request
            pk (integer, opcional): Primary Key

        Returns:
            JSON: Plantilla de rol de proyecto
        """
        try:
            usuario_request = Usuario.objects.get(user=request.user)
            if not usuario_request.tiene_permiso("ver_permisos") or \
               not usuario_request.tiene_permiso("ver_plantillas") or \
               not usuario_request.tiene_permiso("modificar_plantillas"):
                response = {
                    "message": "No tiene permiso para realizar esta acción",
                    "permission_required": [
                        "ver_permisos",
                        "ver_plantillas",
                        "modificar_plantillas"
                    ]
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            # if (usuario_request.rol.pk == int(pk)):
            #     response = {"message": "No puedes modificar tu propio rol"}
            #     return Response(response, status=status.HTTP_403_FORBIDDEN)
            rol = PlantillaRolProyecto.objects.get(pk=pk)
            rol.nombre = request.data["nombre"]
            rol.save()
            serializer = PlantillaRolProyectoSerializer(rol, many=False)
            return Response(serializer.data)
        except PlantillaRolProyecto.DoesNotExist:
            response = {"message": "No existe la plantilla de rol"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=["GET"])
    def permisos(self, request, pk=None):
        """
        permisos Lista los permisos de una plantilla de rol de proyecto

            request (Any): request
            pk (integer, opcional): Primary Key

        Returns:
            JSON: Permisos del Rol con la pk especificada
        """
        try:
            usuario_request = Usuario.objects.get(user=request.user)
            if not usuario_request.tiene_permiso("ver_plantillas"):
                response = {
                    "message": "No tiene permiso para realizar esta acción",
                    "permission_required": ["ver_plantillas"]
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            rol = PlantillaRolProyecto.objects.get(pk=pk)
            permisos = rol.permisos.all()
            serializer = PermisoSerializer(permisos, many=True)
            return Response(serializer.data)
        except PlantillaRolProyecto.DoesNotExist:
            response = {"message": "No existe la plantilla de rol"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)

    @permisos.mapping.post
    def agregar_permiso(self, request, pk=None):
        """
        agregar_permiso Agrega un permiso a una plantilla de rol de proyecto

        Args:
            request (Any): request
            pk (integer, opcional): Primary Key

        Returns:
            JSON: Plantilla de rol de proyecto
        """
        try:
            usuario_request = Usuario.objects.get(user=request.user)
            if not (usuario_request.tiene_permiso("ver_permisos")
                    and usuario_request.tiene_permiso("modificar_plantillas")):
                response = {
                    "message": "No tiene permiso para realizar esta acción",
                    "permission_required": [
                        "ver_permisos",
                        "modificar_plantillas"
                    ]
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            form = AgregarPermisoRolForm(request.data)
            if not form.is_valid():
                response = {
                    "message": "Error de validacion",
                    "errors": form.errors
                }
                return Response(response, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            if (usuario_request.rol.pk == int(pk)):
                response = {"message": "No puedes modificar tu propio rol"}
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            rol = PlantillaRolProyecto.objects.get(pk=pk)
            permiso = Permiso.objects.get(pk=request.data["id"])
            rol.agregar_permiso(permiso)
            serializer = PlantillaRolProyectoSerializer(rol, many=False)
            return Response(serializer.data)
        except PlantillaRolProyecto.DoesNotExist:
            response = {"message": "No existe la plantilla de rol"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)

    @permisos.mapping.delete
    def eliminar_permiso(self, request, pk=None):
        """
        eliminar_permiso Elimina un permiso de una plantilla de rol de proyecto

        Args:
            request (Any): request
            pk (integer, opcional): Primary Key
        """
        try:
            usuario_request = Usuario.objects.get(user=request.user)
            if not (usuario_request.tiene_permiso("ver_permisos")
                    and usuario_request.tiene_permiso("modificar_plantillas")):
                response = {
                    "message": "No tiene permiso para realizar esta acción",
                    "permission_required": [
                        "ver_permisos",
                        "modificar_plantillas"
                    ]
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            # if (usuario_request.rol.pk == int(pk)):
            #     response = {"message": "No puedes modificar tu propio rol"}
            #     return Response(response, status=status.HTTP_403_FORBIDDEN)
            rol = PlantillaRolProyecto.objects.get(pk=pk)
            permiso = Permiso.objects.get(pk=request.data["id"])
            if rol.permisos.all().count() < 2:
                response = {"message": "La plantilla de rol no se puede quedar sin permisos"}
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            rol.eliminar_permiso(permiso)
            serializer = PlantillaRolProyectoSerializer(rol, many=False)
            return Response(serializer.data)
        except Permiso.DoesNotExist:
            response = {"message": "No existe el permiso"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except PlantillaRolProyecto.DoesNotExist:
            response = {"message": "No existe la plantilla de rol"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)
