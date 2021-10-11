from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from backend.api.models import Miembro, Sprint, Usuario
from backend.api.serializers import SprintSerializer


class SprintPlanningViewSet(viewsets.ViewSet):
    """
    SprintPlanningViewSet View para el Sprint Planning

    Args:
        views (View): View del módulo Rest Framework
    """

    @action(detail=True, methods=["POST"])
    def iniciar(self, request, pk=None):
        """
        iniciar_sprint_planning Servicio para Iniciar un Sprint Planning

        Args:
            request (Any): Request que se solicita
            pk (int, optional): Primary Key

        Returns:
            JSON: Metadatos del Sprint a Iniciar la Planificación
        """
        try:
            usuario = Usuario.objects.get(user=request.user)
            sprint = Sprint.objects.get(pk=pk)
            miembro = Miembro.objects.get(usuario=usuario, proyecto=sprint.proyecto)
            if not miembro.tiene_permiso("ver_user_stories") or \
               not usuario.tiene_permiso("ver_proyectos") or \
               not miembro.tiene_permiso("ver_miembros") or \
               not miembro.tiene_permiso("ver_sprints") or \
               not miembro.tiene_permiso("planear_sprints"):
                response = {
                    "message": "No tiene permiso para realizar esta acción",
                    "permission_required": [
                        "ver_user_stories",
                        "ver_proyectos",
                        "ver_miembros",
                        "ver_sprints",
                        "planear_sprints"
                    ],
                    "error": "forbidden"
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            if not sprint.estado == "P" or \
               not sprint.estado_sprint_planning == "P":
                response = {
                    "message": "El Sprint debe estar Pendiente, y Pendiente en Planificación",
                    "error": "conflict"
                }
                return Response(response, status=status.HTTP_409_CONFLICT)
            sprint.iniciar_sprint_planning(planificador=miembro)
            serializer = SprintSerializer(sprint, many=False)
            return Response(serializer.data)
        except Sprint.DoesNotExist:
            response = {
                "message": "No existe el Sprint",
                "error": "not_found"
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Miembro.DoesNotExist:
            response = {
                "message": "Usted no es miembro de este Proyecto",
                "error": "forbidden"
            }
            return Response(response, status=status.HTTP_403_FORBIDDEN)
