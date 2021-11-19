from django.db import transaction
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from backend.api.models import Miembro
from backend.api.models.MiembroSprint import MiembroSprint
from backend.api.models.SprintBacklog import SprintBacklog


class MiembroSprintViewSet(viewsets.ViewSet):

    @transaction.atomic
    def destroy(self, request, pk=None):
        """
        destroy Eliminar un miembro de un sprint

        Args:
            request (Any): request que se solicita
            pk (int, optional): Primary key. Defaults to None.

        Returns:
            JSON: Mensaje de confirmación
        """
        try:
            miembro_sprint = MiembroSprint.objects.get(pk=pk)
            proyecto = miembro_sprint.miembro_proyecto.proyecto
            sprint = miembro_sprint.sprint
            miembro_proyecto = Miembro.objects.get(usuario__user=request.user, proyecto=proyecto)
            if not miembro_proyecto.tiene_permiso("modificar_miembros_sprint"):
                response = {
                    "message": "No tiene permiso para realizar esta acción",
                    "permission_required": ["modificar_miembros_sprint"],
                    "error": "forbidden"
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            if not miembro_sprint.sprint.estado == "A":
                response = {
                    "message": "No se puede eliminar un miembro de un Sprint no activo",
                    "error": "forbidden"
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            sbs = SprintBacklog.objects.filter(sprint=sprint, desarrollador=miembro_sprint)
            for sb in sbs:
                sb.desarrollador = None
                sb.save()
            miembro_sprint.delete()
            response = {
                "message": "Miembro eliminado correctamente",
            }
            return Response(response, status=status.HTTP_200_OK)
        except MiembroSprint.DoesNotExist:
            response = {
                "message": "Miembro del Sprint no existe",
                "error": "not_found"
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

    @transaction.atomic
    @action(detail=True, methods=['POST'])
    def reemplazar(self, request, pk=None):
        """
        reemplazar Reemplaza un miembro de un sprint

        Args:
            request (Any): request que se solicita
            pk (int, optional): Primary key. Defaults to None.

        Returns:
            JSON: Mensaje de confirmación
        """
        try:
            miembro_sprint = MiembroSprint.objects.get(pk=pk)
            proyecto = miembro_sprint.miembro_proyecto.proyecto
            sprint = miembro_sprint.sprint
            miembro_proyecto = Miembro.objects.get(usuario__user=request.user, proyecto=proyecto)
            miembro_nuevo = Miembro.objects.get(pk=request.data["miembro"])
            miembro_sprint_nuevo = MiembroSprint.objects.filter(miembro_proyecto=miembro_nuevo, sprint=sprint)
            if len(miembro_sprint_nuevo) > 0:
                response = {
                    "message": "El miembro ya está en el sprint",
                    "error": "bad_request"
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            if not miembro_proyecto.tiene_permiso("modificar_miembros_sprint"):
                response = {
                    "message": "No tiene permiso para realizar esta acción",
                    "permission_required": ["modificar_miembros_sprint"],
                    "error": "forbidden"
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            if not miembro_sprint.sprint.estado == "A":
                response = {
                    "message": "No se puede eliminar un miembro de un Sprint no activo",
                    "error": "forbidden"
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            sbs = SprintBacklog.objects.filter(sprint=sprint, desarrollador=miembro_sprint)
            miembro_sprint_nuevo = MiembroSprint.objects.create(miembro_proyecto=miembro_nuevo, sprint=sprint)
            for sb in sbs:
                sb.desarrollador = miembro_sprint_nuevo
                sb.save()
            miembro_sprint.delete()
            response = {
                "message": "Miembro reemplazado correctamente",
            }
            return Response(response, status=status.HTTP_200_OK)
        except MiembroSprint.DoesNotExist:
            response = {
                "message": "Miembro del Sprint no existe",
                "error": "not_found"
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Miembro.DoesNotExist:
            response = {
                "message": "Miembro nuevo no existe",
                "error": "not_found"
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
