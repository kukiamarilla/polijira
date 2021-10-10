from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.response import Response
from backend.api.models import Usuario, Miembro, Sprint, MiembroSprint
from backend.api.serializers import MiembroSprintSerializer
from backend.api.forms import CreateMiembroSprintForm
from backend.api.decorators import FormValidator
from django.db import transaction
from django.db.models import Q


class MiembroSprintViewSet(viewsets.ViewSet):
    """
    MiembroSprintViewSet View para el modelo MiembroSprint
    """

    def retrieve(self, request, pk=None):
        """
        retrieve Obtiene un miembro del sprint especificado

        Args:
            request (Any): request
            pk (integer, optional): primary key. Defaults to None.

        Returns:
            JSON: Miembro del Sprint especificado
        """
        try:
            usuario = Usuario.objects.get(user=request.user)
            miembro_sprint = MiembroSprint.objects.get(pk=pk)
            sprint = Sprint.objects.get(pk=miembro_sprint.sprint.pk)
            miembro = Miembro.objects.get(usuario=usuario, proyecto=sprint.proyecto)
            if not miembro.tiene_permiso("ver_sprints"):
                response = {
                    "message": "No tiene permiso para realizar esta acción",
                    "permission_required": ["ver_sprints"],
                    "error": "forbidden"
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            serializer = MiembroSprintSerializer(miembro_sprint, many=False)
            return Response(serializer.data)
        except MiembroSprint.DoesNotExist:
            response = {
                "message": "No existe el Miembro en el Sprint especificado",
                "error": "not_found"
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Miembro.DoesNotExist:
            response = {"message": "Usted no es miembro de este proyecto"}
            return Response(response, status=status.HTTP_403_FORBIDDEN)

    @transaction.atomic
    @FormValidator(form=CreateMiembroSprintForm)
    def create(self, request):
        """
        create Crea un miembro sprint

        Args:
            request (Any): request

        Returns:
            JSON: Miembro de sprint creado
        """
        try:
            usuario = Usuario.objects.get(user=request.user)
            sprint = Sprint.objects.get(pk=request.data["sprint"])
            proyecto = sprint.proyecto
            miembro_request = Miembro.objects.get(usuario=usuario, proyecto=proyecto)
            if not (miembro_request.tiene_permiso("ver_sprints") and
                    miembro_request.tiene_permiso("ver_miembros")):
                response = {
                    "message": "No tiene permiso para realizar esta acción",
                    "permission_required": [
                        "ver_sprints",
                        "ver_miembros"
                    ],
                    "error": "forbidden"
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            miembro = Miembro.objects.get(pk=request.data["miembro"])
            miembro_sprint = MiembroSprint.objects.create(miembro_proyecto=miembro, sprint=sprint)
            serializer = MiembroSprintSerializer(miembro_sprint, many=False)
            return Response(serializer.data)
        except Miembro.DoesNotExist:
            response = {"message": "Usted no es miembro de este proyecto"}
            return Response(response, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, pk=None):
        """
        destroy Elimina un miembro sprint

        Args:
            request (Any): request
            pk (integer, opcional): Primary Key del miembro del sprint a eliminar
        """
        try:
            usuario = Usuario.objects.get(user=request.user)
            miembro = MiembroSprint.objects.get(pk=pk)
            miembro_request = Miembro.objects.get(usuario=usuario, proyecto=miembro.sprint.proyecto)
            if not (miembro_request.tiene_permiso("ver_sprints") and
                    miembro_request.tiene_permiso("ver_miembros")):
                response = {
                    "message": "No tiene permiso para realizar esta acción",
                    "permission_required": [
                        "ver_sprints",
                        "ver_miembros"
                    ],
                    "error": "forbidden"
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            miembro.delete()
            response = {"message": "Miembro Sprint eliminado."}
            return Response(response)
        except Miembro.DoesNotExist:
            response = {"message": "Usted no es miembro de este proyecto"}
            return Response(response, status=status.HTTP_403_FORBIDDEN)
        except MiembroSprint.DoesNotExist:
            response = {
                "message": "Miembro Sprint no existe",
                "error": "not_found"
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
