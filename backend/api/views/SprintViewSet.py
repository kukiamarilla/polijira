from datetime import date, timedelta
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from backend.api.models import Miembro, Sprint, Usuario, Proyecto
from backend.api.models.Actividad import Actividad
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
            sprints_activos = Sprint.objects.filter(proyecto=sprint.proyecto, estado="A")
            if len(sprints_activos) > 0:
                response = {
                    "message": "Sprint no se puede activar porque ya existe un sprint activo en el proyecto",
                    "error": "bad_request"
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
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

    @action(detail=True, methods=["GET"])
    def burndown_chart(self, request, pk=None):
        try:
            sprint = Sprint.objects.get(pk=pk)
            usuario = Usuario.objects.get(user=request.user)
            miembro = Miembro.objects.get(usuario=usuario, proyecto=sprint.proyecto)
            if not miembro.tiene_permiso("ver_sprints") or \
               not miembro.tiene_permiso("ver_burndown_chart"):
                response = {
                    "message": "No tiene permiso para realizar esta acción",
                    "permission_required": ["ver_sprints", "ver_burndown_chart"],
                    "error": "forbidden"
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            if sprint.estado == "P":
                response = {
                    "message": "No puedes ver el Burndown Chart de un Sprint Pendiente",
                    "error": "bad_request"
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            burndown_chart = []
            horas_restantes = sum([sb.horas_estimadas for sb in sprint.sprint_backlogs.all()])
            fecha_ini = sprint.fecha_inicio
            fecha_fin = date.today() if sprint.estado == "A" else sprint.fecha_fin_real
            fecha_fin += timedelta(days=1)
            actual = fecha_ini
            while actual <= fecha_fin:
                burndown_chart.append(
                    {
                        "dia": str(actual),
                        "horas_restantes": horas_restantes
                    }
                )
                actividades = Actividad.objects.filter(fecha_creacion=actual, sprint_backlog__sprint=sprint)
                horas_restantes -= sum([act.horas for act in actividades])
                actual += timedelta(days=1)
            return Response(burndown_chart, status=status.HTTP_200_OK)
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
    def finalizar(self, request, pk=None):
        """
        finalizar Finalizar el sprint

        Args:
            request (Any): Request que se solicita
            pk (int, opcional): Primary key. Defaults to None.
        """
        try:
            sprint = Sprint.objects.get(pk=pk)
            usuario = Usuario.objects.get(user=request.user)
            miembro = Miembro.objects.get(usuario=usuario, proyecto=sprint.proyecto)
            if not miembro.tiene_permiso("finalizar_sprints"):
                response = {
                    "message": "No tiene permiso para realizar esta acción",
                    "permission_required": ["finalizar_sprints"],
                    "error": "forbidden"
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            if sprint.estado != "A":
                response = {
                    "message": "Solo puedes finalizar un Sprint Activo",
                    "error": "bad_request"
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            sprint.finalizar()
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
