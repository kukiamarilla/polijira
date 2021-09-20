from rest_framework import viewsets, status
from rest_framework.response import Response
from backend.api.models import Horario, Usuario, Miembro, Proyecto, RolProyecto
from backend.api.serializers import HorarioSerializer, MiembroSerializer
from rest_framework.decorators import action
from django.db import transaction


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
            rol = Miembro.objects.get(pk=pk)
            serializer = MiembroSerializer(rol, many=False)
            return Response(serializer.data)
        except Miembro.DoesNotExist:
            response = {"message": "No existe el miembro"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)

    @transaction.atomic
    def create(self, request):
        """
        create Crea un miembro nuevo

        Args:
            request (Any): request

        Return:
            JSON: Miembro creado
        """
        try:
            usuario = Usuario.objects.get(pk=request.data["usuario"])
            proyecto = Proyecto.objects.get(pk=request.data["proyecto"])
            rol = RolProyecto.objects.get(pk=request.data["rol"])
            if rol.proyecto != proyecto:
                response = {"message": "Rol no pertenece al proyecto"}
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
        except Usuario.DoesNotExist:
            response = {"message": "No existe el usuario"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Proyecto.DoesNotExist:
            response = {"message": "No existe el proyecto"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except RolProyecto.DoesNotExist:
            response = {"message": "No existe el rol"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)

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
            response = {"message": "Miembro Eliminado."}
            return Response(response)
        except Miembro.DoesNotExist:
            response = {"message": "No existe el miembro"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)

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
            if rol.proyecto != miembro.proyecto:  # form
                response = {"message": "Rol no pertenece al proyecto"}
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            miembro.rol = rol
            miembro.save()
            serializer = MiembroSerializer(miembro, many=False)
            return Response(serializer.data)
        except Miembro.DoesNotExist:
            response = {"message": "No existe el miembro"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except RolProyecto.DoesNotExist:  # form
            response = {"message": "No existe el rol"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=["GET"])
    def horario(self, request, pk=None):
        try:
            usuario_request = Usuario.objects.get(user=request.user)
            miembro = Miembro.objects.get(usuario=usuario_request)
            if not miembro.tiene_permiso("ver_miembros"):
                response = {
                    "message": "No tiene permiso para realizar esta accion",
                    "permission_required": ["agregar_miembros"],
                    "error": "forbidden"
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            miembro = Miembro.objects.get(pk=pk)
            serializer = HorarioSerializer(miembro.horario, many=False)
            return Response(serializer.data)

        except Miembro.DoesNotExist:
            response = {
                "message": "No existe el miembro",
                "error": "not_found"
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        # def capacidad(self, request, pk=None):
