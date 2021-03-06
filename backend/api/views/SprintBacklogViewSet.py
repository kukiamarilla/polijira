from rest_framework import status, viewsets
from django.db import transaction
from rest_framework.decorators import action
from rest_framework.response import Response
from backend.api.decorators import FormValidator
from backend.api.forms import ResponderEstimacionForm, MoverUserStoryForm
from backend.api.models import Miembro, MiembroSprint, SprintBacklog, Usuario
from backend.api.notifications.RespuestaEstimacionNotification import RespuestaEstimacionNotification
from backend.api.serializers import SprintBacklogSerializer, ActividadSerializer
from backend.api.notifications import USDoneNotification, USRechazadoNotification


class SprintBacklogViewSet(viewsets.ViewSet):

    @transaction.atomic
    @action(detail=True, methods=["POST"])
    @FormValidator(form=ResponderEstimacionForm)
    def responder_estimacion(self, request, pk=None):
        try:
            usuario = Usuario.objects.get(user=request.user)
            sprint_backlog = SprintBacklog.objects.get(pk=pk)
            miembro = Miembro.objects.get(usuario=usuario, proyecto=sprint_backlog.sprint.proyecto)
            if not sprint_backlog.sprint.estado_sprint_planning == "I":
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
            if not sprint_backlog.sprint.estado == "P":
                response = {
                    "message": "Solo puedes responder una estimación de un Sprint Pendiente",
                    "error": "conflict"
                }
                return Response(response, status=status.HTTP_409_CONFLICT)
            sprint_backlog.user_story.responder(
                sprint_backlog=sprint_backlog,
                horas_estimadas=(int(request.data.get("horas_estimadas")) + int(sprint_backlog.horas_estimadas))/2
            )
            notification = RespuestaEstimacionNotification(sprint_backlog)
            sprint_backlog.sprint.planificador.usuario.notify(notification)
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

    @FormValidator(form=MoverUserStoryForm)
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
            if not miembro_request.tiene_permiso("ver_kanban") \
                or not miembro_request.tiene_permiso("ver_user_stories") \
                or (
                    not sprint_backlog.desarrollador.miembro_proyecto == miembro_request
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
            if sprint_backlog.user_story.estado == "R" or sprint_backlog.user_story.estado == "C":
                response = {
                    "message": "No se puede modificar el kanban de un user story lanzado o cancelado",
                    "error": "forbidden"
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            estado = request.data.get("estado_kanban")
            if estado == "T" and not miembro_request == sprint_backlog.desarrollador.miembro_proyecto:
                notificacion = USRechazadoNotification(sprint_backlog)
                sprint_backlog.desarrollador.miembro_proyecto.usuario.notify(notificacion)
            if estado == "N" and miembro_request == sprint_backlog.desarrollador.miembro_proyecto:
                QAs = Usuario.objects.filter(
                    miembros__rol__permisos__codigo="lanzar_user_stories",
                    miembros__proyecto=sprint_backlog.sprint.proyecto
                )
                notificacion = USDoneNotification(sprint_backlog)
                notificacion.notify_all(QAs)
            sprint_backlog.mover_kanban(estado)
            serializer = SprintBacklogSerializer(sprint_backlog, many=False)
            return Response(serializer.data)
        except SprintBacklog.DoesNotExist:
            response = {
                "message": "SprintBacklog no existe",
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
                "message": "No eres desarrollador de este User Story",
                "error": "unathorized"
            }
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=True, methods=["GET"])
    def actividades(self, request, pk=None):
        """
        actividades Devuelve las actividades de un user story

        Args:
            request (Any): request que se solicita
            pk (int, optional): Primary key. Defaults to None.

        Returns:
            JSON: Metadatos del SprintBacklog
        """
        try:
            sprint_backlog = SprintBacklog.objects.get(pk=pk)
            serializer = ActividadSerializer(sprint_backlog.actividades, many=True)
            return Response(serializer.data)
        except SprintBacklog.DoesNotExist:
            response = {
                "message": "SprintBacklog no existe",
                "error": "not_found"
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['POST'])
    def reasignar(self, request, pk=None):
        """
        reasignar Reasigna un user story a otro desarrollador

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
            miembro_sprint = MiembroSprint.objects.get(
                id=request.data.get("miembro_sprint"), sprint=sprint_backlog.sprint)
            if not miembro_request.tiene_permiso("modificar_miembros_sprint"):
                response = {
                    "message": "No tiene permiso para realizar esta acción",
                    "permission_required": [
                        "modificar_miembro_sprint"
                    ],
                    "error": "forbidden"
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            if sprint_backlog.sprint.estado != 'A':
                response = {
                    "message": "No se puede reasignar un User Story en un sprint que no está activo.",
                    "error": "bad_request"
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            if sprint_backlog.desarrollador:
                response = {
                    "message": "No se puede reasignar un User Story que no está pendiente de asignación.",
                    "error": "bad_request"
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            sprint_backlog.desarrollador = miembro_sprint
            sprint_backlog.save()
            serializer = SprintBacklogSerializer(sprint_backlog, many=False)
            return Response(serializer.data)
        except SprintBacklog.DoesNotExist:
            response = {
                "message": "El User Story no existe en el sprint.",
                "error": "not_found"
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except MiembroSprint.DoesNotExist:
            response = {
                "message": "El Miembro del Sprint no existe",
                "error": "not_found"
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
