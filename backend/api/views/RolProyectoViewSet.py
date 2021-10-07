from django.db import transaction
from backend.api.decorators import FormValidator
from rest_framework.decorators import action
from backend.api.serializers import RolProyectoSerializer, PermisoProyectoSerializer
from backend.api.models import Usuario, Proyecto, PermisoProyecto, RolProyecto, Miembro
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
            usuario_request = Usuario.objects.get(user=request.user)
            rol = RolProyecto.objects.get(pk=pk)
            miembro = Miembro.objects.get(usuario=usuario_request, proyecto=rol.proyecto)
            if not (miembro.tiene_permiso("ver_roles_proyecto") and
                    miembro.tiene_permiso("ver_permisos_proyecto")):
                response = {
                    "message": "No tiene permiso para realizar esta acción",
                    "permission_required": ["ver_roles_proyecto", "ver_permisos_proyecto"]
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            serializer = RolProyectoSerializer(rol, many=False)
            return Response(serializer.data)
        except RolProyecto.DoesNotExist:
            response = {"message": "No existe el rol de proyecto"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Miembro.DoesNotExist:
            response = {"message": "Usted no es miembro de este proyecto"}
            return Response(response, status=status.HTTP_403_FORBIDDEN)

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
            usuario_request = Usuario.objects.get(user=request.user)
            proyecto = Proyecto.objects.get(pk=request.data["proyecto"])
            miembro = Miembro.objects.get(usuario=usuario_request, proyecto=proyecto)
            if not (miembro.tiene_permiso("crear_roles_proyecto") and
                    miembro.tiene_permiso("ver_permisos_proyecto")):
                response = {
                    "message": "No tiene permiso para realizar esta acción",
                    "permission_required": ["crear_roles_proyecto", "ver_permisos_proyecto"]
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            permisos = request.data["permisos"]
            rol = RolProyecto.objects.create(nombre=request.data["nombre"], proyecto=proyecto)
            for p in permisos:
                perm = PermisoProyecto.objects.get(pk=p["id"])
                rol.agregar_permiso(perm)
            serializer = RolProyectoSerializer(rol, many=False)
            return Response(serializer.data)
        except Miembro.DoesNotExist:
            response = {"message": "Usted no es miembro de este proyecto"}
            return Response(response, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, pk=None):
        """
        destroy Elimina un rol de proyecto

        Args:
            request (Any): request
            pk (integer, opcional): Primary Key
        """
        try:
            usuario_request = Usuario.objects.get(user=request.user)
            rol = RolProyecto.objects.get(pk=pk)
            miembro = Miembro.objects.get(usuario=usuario_request, proyecto=rol.proyecto)
            if not (miembro.tiene_permiso("ver_roles_proyecto")
                    and miembro.tiene_permiso("eliminar_roles_proyecto")):
                response = {
                    "message": "No tiene permiso para realizar esta acción",
                    "permission_required": [
                        "ver_roles_proyecto",
                        "eliminar_roles_proyecto"
                    ]
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            if Miembro.objects.filter(rol__pk=pk).count():
                response = {"message": "Rol asignado a un miembro de proyecto, no se puede eliminar"}
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            rol.delete()
            response = {"message": "Rol de Proyecto Eliminado."}
            return Response(response)
        except RolProyecto.DoesNotExist:
            response = {"message": "No existe el rol de proyecto"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Miembro.DoesNotExist:
            response = {"message": "Usted no es miembro de este proyecto"}
            return Response(response, status=status.HTTP_403_FORBIDDEN)

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
            usuario_request = Usuario.objects.get(user=request.user)
            rol = RolProyecto.objects.get(pk=pk)
            miembro = Miembro.objects.get(usuario=usuario_request, proyecto=rol.proyecto)
            if not (miembro.tiene_permiso("ver_permisos_proyecto") and
                    miembro.tiene_permiso("ver_roles_proyecto") and
                    miembro.tiene_permiso("modificar_roles_proyecto")):
                response = {
                    "message": "No tiene permiso para realizar esta acción",
                    "permission_required": [
                        "ver_permisos_proyecto",
                        "ver_roles_proyecto",
                        "modificar_roles_proyecto"
                    ]
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            if (miembro.rol.pk == int(pk)):
                response = {"message": "No puedes modificar tu propio rol"}
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            rol = RolProyecto.objects.get(pk=pk)
            if rol.nombre == "Scrum Master":
                response = {
                    "message": "No se puede modificar el rol Scrum Master",
                    "error": "forbidden"
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            rol_db = RolProyecto.objects.filter(nombre=request.data["nombre"], proyecto=rol.proyecto)
            if len(rol_db) > 0:
                response = {
                    "message": "Ya existe un rol con ese nombre",
                    "error": "forbidden"
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            rol.nombre = request.data["nombre"]
            rol.save()
            serializer = RolProyectoSerializer(rol, many=False)
            return Response(serializer.data)
        except RolProyecto.DoesNotExist:
            response = {"message": "No existe el rol de proyecto"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Miembro.DoesNotExist:
            response = {"message": "Usted no es miembro de este proyecto"}
            return Response(response, status=status.HTTP_403_FORBIDDEN)

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
            usuario_request = Usuario.objects.get(user=request.user)
            rol = RolProyecto.objects.get(pk=pk)
            miembro = Miembro.objects.get(usuario=usuario_request, proyecto=rol.proyecto)
            if not miembro.tiene_permiso("ver_roles_proyecto"):
                response = {
                    "message": "No tiene permiso para realizar esta acción",
                    "permission_required": ["ver_roles_proyecto"]
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            permisos = rol.permisos.all()
            serializer = PermisoProyectoSerializer(permisos, many=True)
            return Response(serializer.data)
        except RolProyecto.DoesNotExist:
            response = {"message": "No existe el rol de proyecto"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Miembro.DoesNotExist:
            response = {"message": "Usted no es miembro de este proyecto"}
            return Response(response, status=status.HTTP_403_FORBIDDEN)

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
            usuario_request = Usuario.objects.get(user=request.user)
            rol = RolProyecto.objects.get(pk=pk)
            miembro = Miembro.objects.get(usuario=usuario_request, proyecto=rol.proyecto)
            if not (miembro.tiene_permiso("ver_permisos_proyecto")
                    and miembro.tiene_permiso("modificar_roles_proyecto")):
                response = {
                    "message": "No tiene permiso para realizar esta acción",
                    "permission_required": [
                        "ver_permisos_proyecto",
                        "modificar_roles_proyecto"
                    ]
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            form = AgregarPermisoRolProyectoForm(request.data)
            if not form.is_valid():
                response = {
                    "message": "Error de validacion",
                    "errors": form.errors
                }
                return Response(response, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            if (miembro.rol.pk == int(pk)):
                response = {"message": "No puedes modificar tu propio rol"}
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            rol = RolProyecto.objects.get(pk=pk)
            if rol.nombre == "Scrum Master":
                response = {
                    "message": "No se puede modificar el rol Scrum Master",
                    "error": "forbidden"
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            permiso = PermisoProyecto.objects.get(pk=request.data["id"])
            rol.agregar_permiso(permiso)
            serializer = RolProyectoSerializer(rol, many=False)
            return Response(serializer.data)
        except RolProyecto.DoesNotExist:
            response = {"message": "No existe el rol de proyecto"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Miembro.DoesNotExist:
            response = {"message": "Usted no es miembro de este proyecto"}
            return Response(response, status=status.HTTP_403_FORBIDDEN)

    @permisos.mapping.delete
    def eliminar_permiso(self, request, pk=None):
        """
        eliminar_permiso Elimina un permiso de un rol de proyecto

        Args:
            request (Any): request
            pk (integer, opcional): Primary Key
        """
        try:
            usuario_request = Usuario.objects.get(user=request.user)
            rol = RolProyecto.objects.get(pk=pk)
            miembro = Miembro.objects.get(usuario=usuario_request, proyecto=rol.proyecto)
            if not (miembro.tiene_permiso("ver_permisos_proyecto")
                    and miembro.tiene_permiso("modificar_roles_proyecto")):
                response = {
                    "message": "No tiene permiso para realizar esta acción",
                    "permission_required": [
                        "ver_permisos_proyecto",
                        "modificar_roles_proyecto"
                    ]
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            if (miembro.rol.pk == int(pk)):
                response = {"message": "No puedes modificar tu propio rol"}
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            rol = RolProyecto.objects.get(pk=pk)
            if rol.nombre == "Scrum Master":
                response = {
                    "message": "No se puede modificar el rol Scrum Master",
                    "error": "forbidden"
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
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
        except Miembro.DoesNotExist:
            response = {"message": "Usted no es miembro de este proyecto"}
            return Response(response, status=status.HTTP_403_FORBIDDEN)
