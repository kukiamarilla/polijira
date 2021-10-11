from rest_framework import viewsets, status
from rest_framework.response import Response
from backend.api.models import Usuario, Miembro, Sprint, MiembroSprint, SprintBacklog
from backend.api.serializers import MiembroSprintSerializer
from backend.api.forms import CreateMiembroSprintForm, EliminarMiembroSprintForm
from backend.api.decorators import FormValidator
from django.db import transaction


class MiembroSprintViewSet(viewsets.ViewSet):
    """
    MiembroSprintViewSet View para el modelo MiembroSprint
    """

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

    # def retrieve(self, request, pk=None):
    #     """
    #     retrieve Obtiene un miembro del sprint especificado

    #     Args:
    #         request (Any): request
    #         pk (integer, optional): primary key. Defaults to None.

    #     Returns:
    #         JSON: Miembro del Sprint especificado
    #     """
    #     try:
    #         usuario = Usuario.objects.get(user=request.user)
    #         miembro_sprint = MiembroSprint.objects.get(pk=pk)
    #         sprint = Sprint.objects.get(pk=miembro_sprint.sprint.pk)
    #         miembro = Miembro.objects.get(usuario=usuario, proyecto=sprint.proyecto)
    #         if not miembro.tiene_permiso("ver_sprints"):
    #             response = {
    #                 "message": "No tiene permiso para realizar esta acción",
    #                 "permission_required": ["ver_sprints"],
    #                 "error": "forbidden"
    #             }
    #             return Response(response, status=status.HTTP_403_FORBIDDEN)
    #         serializer = MiembroSprintSerializer(miembro_sprint, many=False)
    #         return Response(serializer.data)
    #     except MiembroSprint.DoesNotExist:
    #         response = {
    #             "message": "No existe el Miembro en el Sprint especificado",
    #             "error": "not_found"
    #         }
    #         return Response(response, status=status.HTTP_404_NOT_FOUND)
    #     except Miembro.DoesNotExist:
    #         response = {"message": "Usted no es miembro de este proyecto"}
    #         return Response(response, status=status.HTTP_403_FORBIDDEN)

    @transaction.atomic
    @FormValidator(form=CreateMiembroSprintForm)
    @miembros.mapping.post
    def agregar_miembro(self, request, pk=None):
        """
        agregar_miembro Agrega un miembro sprint

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
        destroy Elimina un miembro sprint

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
