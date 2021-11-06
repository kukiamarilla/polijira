from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from backend.api.models import Miembro, Sprint, SprintBacklog, Usuario, Proyecto
from backend.api.serializers import SprintBacklogSerializer, SprintSerializer
from backend.api.decorators import FormValidator
from backend.api.forms import CreateSprintForm, UpdateSprintForm


class SprintViewSet(viewsets.ViewSet):
    """
    SprintViewSet View para el Sprint

    Args:
        viewsets (ViewSet): View del módulo rest_framework
    """

    def retrieve(self, request, pk=None):
        """
        retrieve Obtiene los detalles de un Sprint

        Args:
            request (Any): Request que se solicita
            pk (int, optional): Primary key

        Returns:
            JSON: Metadatos del Sprint
        """
        try:
            usuario = Usuario.objects.get(user=request.user)
            sprint = Sprint.objects.get(pk=pk)
            miembro = Miembro.objects.get(usuario=usuario, proyecto=sprint.proyecto)
            if not miembro.tiene_permiso("ver_sprints"):
                response = {
                    "message": "No tiene permiso para realizar esta acción",
                    "permission_required": ["ver_sprints"],
                    "error": "forbidden"
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
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
                "message": "Usted no es miembro de este proyecto",
                "error": "forbidden"
            }
            return Response(response, status=status.HTTP_403_FORBIDDEN)

    @FormValidator(form=CreateSprintForm)
    def create(self, request):
        """
        create Servicio para Crear un Sprint

        Args:
            request (Any): Request que se solicita

        Returns:
            JSON: Metadatos del Sprint creado
        """
        try:
            usuario = Usuario.objects.get(user=request.user)
            proyecto = Proyecto.objects.get(pk=request.data.get("proyecto"))
            miembro = Miembro.objects.get(usuario=usuario, proyecto=proyecto)
            pendiente = Sprint.objects.filter(proyecto=proyecto, estado="P")
            if not miembro.tiene_permiso("crear_sprints"):
                response = {
                    "message": "No tiene permiso para realizar esta acción",
                    "permission_required": ["crear_sprints"],
                    "error": "forbidden"
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            if(len(pendiente) > 0):
                response = {
                    "message": "No puede haber más de un sprint pendiente.",
                    "error": "conflict"
                }
                return Response(response, status=status.HTTP_409_CONFLICT)
            if Sprint.se_solapa(
                proyecto=proyecto,
                fecha_inicio=request.data.get("fecha_inicio"),
                fecha_fin=request.data.get("fecha_fin")
            ):
                response = {
                    "message": "La fecha indicada coincide con otro Sprint del Proyecto.",
                    "error": "conflict"
                }
                return Response(response, status=status.HTTP_409_CONFLICT)
            sprint = Sprint.create(
                fecha_inicio=request.data.get("fecha_inicio"),
                fecha_fin=request.data.get("fecha_fin"),
                proyecto=request.data.get("proyecto")
            )
            serializer = SprintSerializer(sprint, many=False)
            return Response(serializer.data)
        except Miembro.DoesNotExist:
            response = {
                "message": "Usted no es miembro de este Proyecto",
                "error": "forbidden"
            }
            return Response(response, status=status.HTTP_403_FORBIDDEN)

    @FormValidator(form=UpdateSprintForm)
    def update(self, request, pk=None):
        """
        update Servicio para modificar un Sprint

        Args:
            request (Any): Request que se solicita
            pk (int, optional): Primary Key

        Returns:
            JSON: Metadatos del Sprint
        """
        try:
            usuario = Usuario.objects.get(user=request.user)
            sprint = Sprint.objects.get(pk=pk)
            miembro = Miembro.objects.get(usuario=usuario, proyecto=sprint.proyecto)
            if not miembro.tiene_permiso("ver_sprints") or \
               not miembro.tiene_permiso("modificar_sprints"):
                response = {
                    "message": "No tiene permiso para realizar esta acción",
                    "permission_required": [
                        "ver_sprints",
                        "modificar_sprints"
                    ],
                    "error": "forbidden"
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            if not sprint.estado == "P":
                response = {
                    "message": "El Sprint no se encuentra en estado Pendiente",
                    "error": "conflict"
                }
                return Response(response, status=status.HTTP_409_CONFLICT)
            if Sprint.se_solapa(
                proyecto=sprint.proyecto,
                fecha_inicio=request.data.get("fecha_inicio"),
                fecha_fin=request.data.get("fecha_fin")
            ):
                response = {
                    "message": "La fecha indicada coincide con otro Sprint del Proyecto.",
                    "error": "conflict"
                }
                return Response(response, status=status.HTTP_409_CONFLICT)
            sprint.update(
                fecha_inicio=request.data.get("fecha_inicio"),
                fecha_fin=request.data.get("fecha_fin")
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

    def destroy(self, request, pk=None):
        """
        destroy Servicio para eliminar un Sprint

        Args:
            request (Any): Request que se solicita
            pk (int, optional): Primary Key
        Returns:
            JSON: Mensaje de Eliminación Exitosa
        """
        try:
            usuario = Usuario.objects.get(user=request.user)
            sprint = Sprint.objects.get(pk=pk)
            miembro = Miembro.objects.get(usuario=usuario, proyecto=sprint.proyecto)
            if not miembro.tiene_permiso("ver_sprints") or \
               not miembro.tiene_permiso("eliminar_sprints"):
                response = {
                    "message": "No tiene permiso para realizar esta acción",
                    "permission_required": [
                        "ver_sprints",
                        "eliminar_sprints"
                    ],
                    "error": "forbidden"
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            if not sprint.estado == "P":
                response = {
                    "message": "El Sprint no se encuentra en estado Pendiente",
                    "error": "conflict"
                }
                return Response(response, status=status.HTTP_409_CONFLICT)
            sprint.delete()
            response = {
                "message": "Sprint Eliminado"
            }
            return Response(response, status=status.HTTP_200_OK)
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
    def sprint_backlogs(self, request, pk=None):
        """
        sprint_backlogs Servicio para listar los Sprint Backlogs de un Sprint

        Args:
            request (Any): Request que se solicita
            pk (int, optional): Primary Key
        Returns:
            JSON -> list: Todos los Sprint Backlogs del Sprint
        """
        try:
            usuario = Usuario.objects.get(user=request.user)
            sprint = Sprint.objects.get(pk=pk)
            miembro = Miembro.objects.get(usuario=usuario, proyecto=sprint.proyecto)
            if not miembro.tiene_permiso("ver_sprints") or \
               not miembro.tiene_permiso("ver_user_stories"):
                response = {
                    "message": "No tienes permiso para realizar esta acción",
                    "error": "forbidden"
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            serializer = SprintBacklogSerializer(sprint.sprint_backlogs.all(), many=True)
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

    @action(detail=True, methods=["POST"])
    def activar(self, request, pk=None):
        """
        activar Servicio para activar sprint

        Args:
            request (Any): Request que se solicita
            pk (int, opcional): Primary key. Defaults to None.
        """
        try:
            usuario = Usuario.objects.get(user=request.user)
            sprint = Sprint.objects.get(pk=pk)
            miembro = Miembro.objects.get(usuario=usuario, proyecto=sprint.proyecto)
            if not (miembro.tiene_permiso("ver_sprints") and
                    miembro.tiene_permiso("activar_sprints")):
                response = {
                    "message": "No tienes permiso para realizar esta acción",
                    "permission_required": [
                        "ver_sprints",
                        "activar_sprints"
                    ],
                    "error": "forbidden"
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            if sprint.estado_sprint_planning != 'F':
                response = {
                    "message": "Sprint Planning aún no fue finalizado",
                    "error": "forbidden"
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            if sprint.estado != 'P':
                response = {
                    "message": "Sprint no se puede activar en el estado actual",
                    "error": "forbidden"
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            sprint.activar()
            serializer = SprintSerializer(sprint, many=False)
            return Response(serializer.data)
        except Sprint.DoesNotExist:
            response = {
                "message": "No existe el Sprint especificado",
                "error": "not_found"
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Miembro.DoesNotExist:
            response = {
                "message": "Usted no es miembro de este Proyecto",
                "error": "forbidden"
            }
            return Response(response, status=status.HTTP_403_FORBIDDEN)
