from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from backend.api.models import Miembro, Sprint, Usuario
from backend.api.serializers import SprintSerializer
from backend.api.decorators import FormValidator
from backend.api.forms import CreateSprintForm


class SprintViewSet(viewsets.ViewSet):
    """
    SprintPlanningViewSet View para el Sprint Planning

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
            JSON: Metados del Sprint
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
        try:
            usuario = Usuario.objects.get(user=request.user)
            miembro = Miembro.objects.get(usuario=usuario, proyecto=request.data.get("proyecto"))
            if not miembro.tiene_permiso("crear_sprints"):
                response = {
                    "message": "No tiene permiso para realizar esta acción",
                    "permission_required": ["crear_sprints"],
                    "error": "forbidden"
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            sprint = Sprint.create(
                fecha_inicio=request.data.get("fecha_inicio"),
                fecha_fin=request.data.get("fecha_fin"),
                capacidad=request.data.get("capacidad"),
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
