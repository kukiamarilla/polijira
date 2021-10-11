from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db import transaction
from backend.api.models import Miembro, MiembroSprint, ProductBacklog, Sprint, SprintBacklog, UserStory, Usuario
from backend.api.serializers import SprintSerializer, MiembroSprintSerializer
from backend.api.decorators import FormValidator
from backend.api.forms import PlanificarUserStoryForm, CreateMiembroSprintForm, EliminarMiembroSprintForm


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

    @action(detail=True, methods=["GET"])
    def miembros(self, request, pk=None):
        """
        miembros Lista los miembros de un sprint

        Args:
            request (Any): request
            pk (integer, optional): primary key. Defaults to None.
        """
        try:
            usuario = Usuario.objects.get(user=request.user)
            sprint = Sprint.objects.get(pk=pk)
            miembro = Miembro.objects.get(usuario=usuario, proyecto=sprint.proyecto)
            if not (miembro.tiene_permiso("ver_sprints") and
                    miembro.tiene_permiso("ver_miembros") and
                    miembro.tiene_permiso("ver_miembros_sprint")):
                response = {
                    "message": "No tiene permiso para realizar esta acción",
                    "permission_required": [
                        "ver_sprints",
                        "ver_miembros",
                        "ver_miembros_sprint"
                    ],
                    "error": "forbidden"
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            miembro_sprint = MiembroSprint.objects.filter(sprint=sprint)
            serializer = MiembroSprintSerializer(miembro_sprint, many=True)
            return Response(serializer.data)
        except Miembro.DoesNotExist:
            response = {
                "message": "Usted no es miembro de este proyecto",
                "error": "forbidden"
            }
            return Response(response, status=status.HTTP_403_FORBIDDEN)
        except Sprint.DoesNotExist:
            response = {
                "message": "Sprint especificado no existe",
                "error": "not_found"
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

    @transaction.atomic
    @FormValidator(form=CreateMiembroSprintForm)
    @miembros.mapping.post
    def agregar_miembro(self, request, pk=None):
        """
        agregar_miembro Agrega un miembro de un sprint

        Args:
            request (Any): request

        Returns:
            JSON: Miembro de sprint agregado
        """
        try:
            usuario = Usuario.objects.get(user=request.user)
            sprint = Sprint.objects.get(pk=pk)
            proyecto = sprint.proyecto
            miembro_request = Miembro.objects.get(usuario=usuario, proyecto=proyecto)
            if sprint.estado_sprint_planning != 'I':
                response = {
                    "message": "Planificación del sprint no fue iniciada",
                    "error": "forbidden"
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            if sprint.planificador != miembro_request:
                response = {
                    "message": "Usted no es el planificador de sprint",
                    "error": "forbidden"
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            miembro = Miembro.objects.get(pk=request.data["miembro"])
            if miembro.proyecto != proyecto:
                response = {
                    "message": "El miembro no pertenece a este proyecto",
                    "error": "bad_request"
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            sprint_backlog = SprintBacklog.objects.filter(sprint=sprint)
            if len(sprint_backlog) > 0:
                response = {
                    "message": "Este paso ya se completó",
                    "error": "bad_request"
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            miembro_sprint = MiembroSprint.objects.filter(miembro_proyecto=miembro, sprint=sprint)
            if len(miembro_request) > 0:
                response = {
                    "message": "Este miembro ya fue agregado al Sprint",
                    "error": "bad_request"
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            miembro_sprint = MiembroSprint.objects.create(miembro_proyecto=miembro, sprint=sprint)
            serializer = MiembroSprintSerializer(miembro_sprint, many=False)
            return Response(serializer.data)
        except Miembro.DoesNotExist:
            response = {
                "message": "Usted no es miembro de este proyecto",
                "error": "forbidden"
            }
            return Response(response, status=status.HTTP_403_FORBIDDEN)
        except Sprint.DoesNotExist:
            response = {
                "message": "No existe el Sprint especificado",
                "error": "not_found"
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

    @FormValidator(form=EliminarMiembroSprintForm)
    @miembros.mapping.delete
    def eliminar_miembros(self, request, pk=None):
        """
        destroy Elimina un miembro de un sprint

        Args:
            request (Any): request
            pk (integer, opcional): Primary Key del miembro del sprint a eliminar
        """
        try:
            usuario = Usuario.objects.get(user=request.user)
            sprint = Sprint.objects.get(pk=pk)
            proyecto = sprint.proyecto
            miembro_request = Miembro.objects.get(usuario=usuario, proyecto=proyecto)
            if sprint.estado_sprint_planning != 'I':
                response = {
                    "message": "Planificación del sprint no fue iniciada",
                    "error": "forbidden"
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            if sprint.planificador != miembro_request:
                response = {
                    "message": "Usted no es el planificador de sprint",
                    "error": "forbidden"
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            miembro_sprint = MiembroSprint.objects.get(pk=request.data["miembro_sprint"])
            if miembro_sprint.sprint != sprint:
                response = {
                    "message": "El miembro sprint no pertenece a este sprint",
                    "error": "bad_request"
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            sprint_backlog = SprintBacklog.objects.filter(sprint=sprint)
            if len(sprint_backlog) > 0:
                response = {
                    "message": "Este paso ya se completó",
                    "error": "bad_request"
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            miembro_sprint.delete()
            response = {"message": "Miembro Sprint eliminado."}
            return Response(response)
        except Miembro.DoesNotExist:
            response = {
                "message": "Usted no es miembro de este proyecto",
                "error": "forbidden"
            }
            return Response(response, status=status.HTTP_403_FORBIDDEN)
        except Sprint.DoesNotExist:
            response = {
                "message": "No existe el Sprint especificado",
                "error": "not_found"
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

    @transaction.atomic
    @action(detail=True, methods=["POST"])
    @FormValidator(form=PlanificarUserStoryForm)
    def planificar_user_story(self, request, pk=None):
        try:
            usuario = Usuario.objects.get(user=request.user)
            sprint = Sprint.objects.get(pk=pk)
            miembro = Miembro.objects.get(usuario=usuario, proyecto=sprint.proyecto)
            if not sprint.estado_sprint_planning == "I":
                response = {
                    "message": "Debe Iniciar la Planificación de este Sprint",
                    "error": "conflict"
                }
                return Response(response, status=status.HTTP_409_CONFLICT)
            if not sprint.planificador.id == miembro.id:
                response = {
                    "message": "No tiene permiso para realizar esta acción",
                    "error": "forbidden"
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            product_backlog = ProductBacklog.objects.get(
                proyecto=sprint.proyecto, user_story_id=request.data.get("user_story"))
            sprint.planificar(
                user_story=product_backlog.user_story,
                horas_estimadas=request.data.get("horas_estimadas"),
                desarrollador=MiembroSprint.objects.get(
                    miembro_proyecto_id=request.data.get("desarrollador"), sprint=sprint),
                sprint_backlog_handler=SprintBacklog.agregar_user_story,
                product_backlog_handler=ProductBacklog.eliminar_user_story
            )
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
        except MiembroSprint.DoesNotExist:
            response = {
                "message": "El miembro asignado como desarrollador no es miembro de este Sprint",
                "error": "bad_request"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except ProductBacklog.DoesNotExist:
            response = {
                "message": "El User Story no pertenece a este Proyecto",
                "error": "bad_request"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
