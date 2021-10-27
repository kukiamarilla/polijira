from rest_framework import status, views
from django.db import transaction
from rest_framework.decorators import action
from rest_framework.response import Response

from backend.api.decorators import FormValidator
from backend.api.forms import ResponderEstimacionForm
from backend.api.models import Miembro, SprintBacklog, Usuario, RegistroUserStory
from backend.api.serializers import SprintBacklogSerializer


class SprintBacklogViewSet(views.View):

    @transaction.atomic
    @action(detail=True, methods=["POST"])
    @FormValidator(form=ResponderEstimacionForm)
    def responder_estimacion(self, request, pk=None):
        try:
            usuario = Usuario.objects.get(user=request.user)
            sprint_backlog = SprintBacklog.objects.get(pk=pk)
            sprint = sprint_backlog.sprint
            miembro = Miembro.objects.get(usuario=usuario, proyecto=sprint.proyecto)
            if not sprint.estado_sprint_planning == "I":
                response = {
                    "message": "Un Planificador debe Iniciar el Sprint Planning para responder una estimación",
                    "error": "bad_request"
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            if not sprint_backlog.estado_estimacion == "p":
                response = {
                    "message": "Este User Story aun no fue estimado por el Planificador",
                    "error": "bad_request"
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            if not sprint_backlog.desarrollador and not miembro == sprint_backlog.desarrollador.miembro_proyecto:
                response = {
                    "message": "Usted no es desarrollador de este User Story",
                    "error": "bad_request"
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            if not sprint.estado == "P":
                response = {
                    "message": "Solo puedes responder una estimación de un Sprint Pendiente",
                    "error": "conflict"
                }
                return Response(response, status=status.HTTP_409_CONFLICT)
            sprint_backlog.update(
                horas_estimadas=(int(request.data.get("horas_estimadas")) + int(sprint_backlog.horas_estimadas))/2,
                estado_estimacion="C"
            )
            serializer = SprintBacklogSerializer(sprint_backlog, many=False)
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
