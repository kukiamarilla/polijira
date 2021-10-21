from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from backend.api.models import Miembro, Sprint, Usuario, UserStory, SprintBacklog
from backend.api.models.MiembroSprint import MiembroSprint
from backend.api.serializers import SprintBacklogSerializer
from backend.api.decorators import FormValidator
from backend.api.forms import MoverKanbanForm


class SprintBacklogViewSet(viewsets.ViewSet):
    """
    SprintBacklogViewSet View para el Sprint Backlog

    Args:
        viewsets (ViewSet): View del módulo rest_framework
    """

    @FormValidator(form=MoverKanbanForm)
    @action(detail=True, methods=["POST"])
    def mover(self, request, pk=None):
        """
        mover Mueve un user story a otra columna de kanban

        Args:
            request (Any): request que se solicita
            pk (int, optional): Primary key. Defaults to None.

        Returns:
            JSON: Metadatos del SprintBacklog
        """
        try:
            usuario_request = Usuario.objects.get(user=request.user)
            sprint_backlog = SprintBacklog.objects.get(pk=pk)
            miembro_request = Miembro.objects.get(usuario=usuario_request, proyecto=sprint_backlog.sprint.proyecto)
            miembro_sprint = MiembroSprint.objects.get(miembro_proyecto=miembro_request, sprint=sprint_backlog.sprint)
            if not miembro_request.tiene_permiso("ver_kanban") \
                or not miembro_request.tiene_permiso("ver_user_stories") \
                or (
                    not sprint_backlog.user_story.desarrollador == miembro_sprint
                    and not miembro_request.tiene_permiso("mover_user_stories")
            ):
                response = {
                    "message": "No tiene permiso para realizar esta acción",
                    "permission_required": [
                        "ver_kanban",
                        "ver_user_stories",
                        "mover_user_stories"
                    ],
                    "error": "forbidden"
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            if sprint_backlog.sprint.estado != 'A':
                response = {
                    "message": "El kanban no se puede modificar en el estado actual del Sprint",
                    "error": "forbidden"
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            estado = request.data.get("estado_kanban")
            sprint_backlog.mover_kanban(estado)
            serializer = SprintBacklogSerializer(sprint_backlog, many=False)
            return Response(serializer.data)
        except Miembro.DoesNotExist:
            response = {
                "message": "Usted no es miembro de este Proyecto",
                "error": "forbidden"
            }
            return Response(response, status=status.HTTP_403_FORBIDDEN)
        except SprintBacklog.DoesNotExist:
            response = {
                "message": "SprintBacklog no existe",
                "error": "not_found"
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
