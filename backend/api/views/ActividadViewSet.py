from rest_framework import status, viewsets
from rest_framework.response import Response
from datetime import date
from backend.api.models import Actividad, Miembro, MiembroSprint, SprintBacklog, Usuario, UserStory
from backend.api.serializers import ActividadSerializer


class ActividadViewSet(viewsets.ViewSet):
    """
    ActividadViewSet View para Actividad

    Args:
        viewsets (ViewSet): View del módulo Rest Framework
    """

    def create(self, request):
        try:

            usuario = Usuario.objects.get(user=request.user)
            sprint_backlog = SprintBacklog.objects.get(request.data.get("sprint_backlog"))
            miembro_proyecto = Miembro.objects.get(
                usuario=usuario,
                proyecto=sprint_backlog.sprint.proyecto
            )
            miembro_sprint = MiembroSprint.objects.get(
                miembro_proyecto=miembro_proyecto,
                sprint=sprint_backlog.sprint
            )
            if not sprint_backlog.desarrollador == miembro_sprint:
                response = {
                    "message": "Usted no es desarrollador del User Story",
                    "error": "forbidden"
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            if not sprint_backlog.sprint.estado == "A":
                response = {
                    "message": "Para registrar una actividad el Sprint debe estar Activo",
                    "error": "bad_request"
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            actividad = Actividad.objects.create(
                descripcion=request.data.get("descripcion"),
                horas=request.data.get("horas"),
                fecha_creacion=date.today(),
                user_story=sprint_backlog.user_story,
                desarrollador=usuario
            )
            serializer = ActividadSerializer(actividad, many=False)
            return Response(serializer.data)

        except SprintBacklog.DoesNotExist:
            response = {
                "message": "No existe el Sprint Backlog",
                "error": "not_found"
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Miembro.DoesNotExist:
            response = {
                "message": "Usted no es miembro de este Proyecto",
                "error": "forbidden"
            }
            return Response(response, status=status.HTTP_403_FORBIDDEN)
        except MiembroSprint.DoesNotExist:
            response = {
                "message": "Usted no es miembro de este Sprint",
                "error": "forbidden"
            }
            return Response(response, status=status.HTTP_403_FORBIDDEN)
