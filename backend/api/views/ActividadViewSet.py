from rest_framework import status, viewsets
from rest_framework.response import Response
from datetime import date
from backend.api.models import Actividad, Miembro, MiembroSprint, SprintBacklog, Usuario, UserStory
from backend.api.serializers import ActividadSerializer
from backend.api.decorators import FormValidator
from backend.api.forms import CreateActividadForm


class ActividadViewSet(viewsets.ViewSet):
    """
    ActividadViewSet View para Actividad

    Args:
        viewsets (ViewSet): View del módulo Rest Framework
    """

    @FormValidator(form=CreateActividadForm)
    def create(self, request):
        """
        create Registra una Actividad del Desarrollador

        Args:
            request (Any): Contiene: id del Sprint Backlog, horas dedicadas, y una descripcion

        Returns:
            JSON: Actividad
        """
        try:
            usuario = Usuario.objects.get(user=request.user)
            sprint_backlog = SprintBacklog.objects.get(pk=request.data.get("sprint_backlog"))
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
                sprint_backlog=sprint_backlog,
                desarrollador=usuario
            )
            serializer = ActividadSerializer(actividad, many=False)
            return Response(serializer.data)
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

    def update(self, request, pk=None):
        """
        update Modifica una Actividad realizada

        Args:
            request (Any): Contiene: hora a modificar, descripcion a modificar
            pk (int, optional): id de Actividad a modificar

        Returns:
            JSON: Actividad modificada
        """
        try:
            usuario = Usuario.objects.get(user=request.user)
            actividad = Actividad.objects.get(pk=pk)
            if not usuario == actividad.desarrollador:
                response = {
                    "message": "Usted no es desarrollador de esta Actividad",
                    "error": "forbidden"
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            actividad.update(
                horas=request.data.get("horas"),
                descripcion=request.data.get("descripcion")
            )
            serializer = ActividadSerializer(actividad)
            return Response(serializer.data)
        except Actividad.DoesNotExist:
            response = {
                "message": "No existe la Actividad",
                "error": "not_found"
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        """
        destroy Elimina una Actividad

        Args:
            request (Any): Contiene: Usuario que solicita el servicio de eliminar
            pk (int, optional): id de la Actividad a eliminar

        Returns:
            JSON: Mensaje de Eliminacion Exitosa
        """
        try:
            usuario = Usuario.objects.get(user=request.user)
            actividad = Actividad.objects.get(pk=pk)
            if not usuario == actividad.desarrollador:
                response = {
                    "message": "Usted no es desarrollador de esta Actividad",
                    "error": "forbidden"
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            actividad.delete()
            response = {
                "message": "Actividad Eliminada"
            }
            return Response(response, status=status.HTTP_200_OK)
        except Actividad.DoesNotExist:
            response = {
                "message": "No existe la Actividad",
                "error": "not_found"
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
