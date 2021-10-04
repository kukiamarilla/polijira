from rest_framework import viewsets, status
from rest_framework.response import Response
from backend.api.models import Usuario, Miembro, Proyecto, RolProyecto, Horario
from backend.api.serializers import MiembroSerializer, HorarioSerializer
from rest_framework.decorators import action
from django.db import transaction
from backend.api.decorators import FormValidator
from backend.api.forms import CreateMiembroForm, UpdateMiembroForm


class MiembroViewSet(viewsets.ViewSet):
    """
    MiembroViewSet View para el modelo de Miembro

    Args:
        viewsets (ViewSet): Tipo de clase basado en View
    """

    def retrieve(self, request, pk=None):
        """
        retrieve Obtiene un miembro por su pk

        Args:
            request (Any): request
            pk (integer, opcional): Primary Key

        Return:
            JSON: Miembro con la pk especificada
        """
        try:
            usuario_request = Usuario.objects.get(user=request.user)
            miembro = Miembro.objects.get(pk=pk)
            miembro_request = Miembro.objects.filter(usuario=usuario_request, proyecto=miembro.proyecto)
            if miembro_request.count() != 1:
                response = {"message": "Usted no es miembro de este proyecto"}
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            if not miembro_request[0].tiene_permiso("ver_miembros"):
                response = {
                    "message": "No tiene permiso para realizar esta acción",
                    "permission_required": ["ver_miembros"]
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            serializer = MiembroSerializer(miembro, many=False)
            return Response(serializer.data)
        except Miembro.DoesNotExist:
            response = {
                "message": "No existe el miembro",
                "error": "not_found"
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

    @transaction.atomic
    @FormValidator(form=CreateMiembroForm)
    def create(self, request):
        """
        create Crea un miembro nuevo

        Args:
            request (Any): request

        Return:
            JSON: Miembro creado
        """
        try:
            usuario_request = Usuario.objects.get(user=request.user)
            proyecto = Proyecto.objects.get(pk=request.data["proyecto"])
            miembro_request = Miembro.objects.get(usuario=usuario_request, proyecto=proyecto)
            if not (miembro_request.tiene_permiso("agregar_miembros") and
                    miembro_request.tiene_permiso("ver_roles_proyecto") and
                    usuario_request.tiene_permiso("ver_usuarios")):
                response = {
                    "message": "No tiene permiso para realizar esta acción",
                    "permission_required": [
                        "agregar_miembros",
                        "ver_roles_proyecto",
                        "ver_usuarios"
                    ]
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            usuario = Usuario.objects.get(pk=request.data["usuario"])
            rol = RolProyecto.objects.get(pk=request.data["rol"])
            miembro = Miembro.objects.create(usuario=usuario, proyecto=proyecto, rol=rol)
            horario = Horario.objects.create(
                lunes=request.data["horario"]["lunes"],
                martes=request.data["horario"]["martes"],
                miercoles=request.data["horario"]["miercoles"],
                jueves=request.data["horario"]["jueves"],
                viernes=request.data["horario"]["viernes"],
                sabado=request.data["horario"]["sabado"],
                domingo=request.data["horario"]["domingo"]
            )
            horario.asignar_horario(miembro)
            serializer = MiembroSerializer(miembro, many=False)
            return Response(serializer.data)
        except Miembro.DoesNotExist:
            response = {"message": "Usted no es miembro de este proyecto"}
            return Response(response, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, pk=None):
        """
        destroy Elimina un miembro con la pk especificada

        Args:
            request (Any): request
            pk (integer, opcional): Primary Key del miembro a eliminar
        """
        try:
            usuario_request = Usuario.objects.get(user=request.user)
            miembro = Miembro.objects.get(pk=pk)
            miembro_request = Miembro.objects.filter(usuario=usuario_request, proyecto=miembro.proyecto)
            if miembro_request.count() != 1:
                response = {"message": "Usted no es miembro de este proyecto"}
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            if not (miembro_request[0].tiene_permiso("eliminar_miembros") and
                    miembro_request[0].tiene_permiso("ver_roles_proyecto") and
                    usuario_request.tiene_permiso("ver_usuarios")):
                response = {
                    "message": "No tiene permiso para realizar esta acción",
                    "permission_required": [
                        "eliminar_miembros",
                        "ver_roles_proyecto",
                        "ver_usuarios"
                    ],
                    "error": "forbidden"
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            if miembro_request[0].id == miembro.id:
                response = {
                    "message": "No puedes eliminarte a ti mismo",
                    "error": "bad_request"
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            if miembro.rol.nombre == "Scrum Master":
                response = {
                    "message": "No se puede eliminar el miembro Scrum Master",
                    "error": "forbidden"
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            miembro.delete()
            response = {"message": "Miembro Eliminado"}
            return Response(response)
        except Miembro.DoesNotExist:
            response = {
                "message": "No existe el miembro",
                "error": "not_found"
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

    @FormValidator(form=UpdateMiembroForm)
    def update(self, request, pk=None):
        """
        update Modifica un miembro con la pk especificada

        Args:
            request (Any): request
            pk (integer, opcional): Primary key del miembro a modificar
        """
        try:
            usuario_request = Usuario.objects.get(user=request.user)
            miembro = Miembro.objects.get(pk=pk)
            miembro_request = Miembro.objects.filter(usuario=usuario_request, proyecto=miembro.proyecto)
            if miembro_request.count() != 1:
                response = {"message": "Usted no es miembro de este proyecto"}
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            if not (miembro_request[0].tiene_permiso("modificar_miembros") and
                    miembro_request[0].tiene_permiso("ver_roles_proyecto") and
                    usuario_request.tiene_permiso("ver_usuarios")):
                response = {
                    "message": "No tiene permiso para realizar esta acción",
                    "permission_required": [
                        "modificar_miembros",
                        "ver_roles_proyecto",
                        "ver_usuarios"
                    ]
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            if miembro_request[0].id == miembro.id:
                response = {
                    "message": "No puedes modificar tu rol",
                    "error": "bad_request"
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            if miembro.rol.nombre == "Scrum Master":
                response = {
                    "message": "No se puede modificar el miembro Scrum Master",
                    "error": "forbidden"
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            rol = RolProyecto.objects.get(pk=request.data["rol"])
            if rol.proyecto != miembro.proyecto:
                response = {
                    "message": "El rol no pertenece a este proyecto",
                    "error": "forbidden"
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            miembro.rol = rol
            miembro.save()
            serializer = MiembroSerializer(miembro, many=False)
            return Response(serializer.data)
        except Miembro.DoesNotExist:
            response = {
                "message": "No existe el miembro",
                "error": "not_found"
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=["GET"])
    def horario(self, request, pk=None):
        try:
            usuario_request = Usuario.objects.get(user=request.user)
            miembro = Miembro.objects.get(pk=pk)
            miembro_request = Miembro.objects.filter(usuario=usuario_request, proyecto=miembro.proyecto)
            if miembro_request.count() != 1:
                response = {"message": "Usted no es miembro de este proyecto"}
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            if not miembro_request[0].tiene_permiso("ver_miembros"):
                response = {
                    "message": "No tiene permiso para realizar esta accion",
                    "permission_required": ["ver_miembros"],
                    "error": "forbidden"
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            serializer = HorarioSerializer(miembro.horario, many=False)
            return Response(serializer.data)

        except Miembro.DoesNotExist:
            response = {
                "message": "No existe el miembro",
                "error": "not_found"
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        # def capacidad(self, request, pk=None):
