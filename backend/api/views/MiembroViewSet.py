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
            miembro_propio = Miembro.objects.get(usuario=usuario_request, proyecto=miembro.proyecto)
            if not miembro_propio.tiene_permiso("ver_miembros"):
                response = {
                    "message": "No tiene permiso para realizar esta acción",
                    "permission_required": ["ver_miembros"]
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            serializer = MiembroSerializer(miembro, many=False)
            return Response(serializer.data)
        except Miembro.DoesNotExist:
            response = {"message": "Usted no es miembro de este proyecto"}
            return Response(response, status=status.HTTP_403_FORBIDDEN)

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
        usuario = Usuario.objects.get(pk=request.data["usuario"])
        proyecto = Proyecto.objects.get(pk=request.data["proyecto"])
        rol = RolProyecto.objects.get(pk=request.data["rol"])
        if rol.proyecto != proyecto:
            response = {
                "message": "El rol no pertenece a este proyecto",
                "error": "forbidden"
            }
            return Response(response, status=status.HTTP_403_FORBIDDEN)
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

    def destroy(self, request, pk=None):
        """
        destroy Elimina un miembro con la pk especificada

        Args:
            request (Any): request
            pk (integer, opcional): Primary Key del miembro a eliminar
        """
        try:
            miembro = Miembro.objects.get(pk=pk)
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
            miembro = Miembro.objects.get(pk=pk)
            rol = RolProyecto.objects.get(pk=request.data["rol"])
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
            miembro_request = Miembro.objects.get(usuario=usuario_request, proyecto=miembro.proyecto)
            if not miembro_request.tiene_permiso("ver_miembros"):
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
