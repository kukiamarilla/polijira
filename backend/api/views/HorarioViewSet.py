from rest_framework import viewsets, status
from rest_framework.response import Response
from backend.api.models import Usuario, Miembro, Horario
from backend.api.serializers import HorarioSerializer
from backend.api.decorators import FormValidator
from backend.api.forms import UpdateHorarioForm


class HorarioViewSet(viewsets.ViewSet):
    """
    HorarioViewSet View para el modelo Horario

    Args:
        viewsets (ViewSet): View del modulo rest_framework
    """

    @FormValidator(form=UpdateHorarioForm)
    def update(self, request, pk=None):
        """
        update Modifica un horario

        Args:
            request (JSON): Dias con horas que va a trabajar cada día
            pk (int, optional): Primary key del horario a ser modificado. Defaults to None.
        """
        try:
            usuario_request = Usuario.objects.get(user=request.user)
            horario = Horario.objects.get(pk=pk)
            miembro = Miembro.objects.get(usuario=usuario_request, proyecto=horario.miembro.proyecto)
            if not miembro.tiene_permiso("modificar_miembros"):
                response = {
                    "message": "No tiene permiso para realizar esta accion",
                    "permission_required": ["modificar_miembros"],
                    "error": "forbidden"
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            Horario.objects.filter(pk=pk).update(**request.data)
            horario = Horario.objects.get(pk=pk)
            serializer = HorarioSerializer(horario, many=False)
            return Response(serializer.data)
        except Horario.DoesNotExist:
            response = {
                "message": "No existe el horario",
                "error": "not_found"
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
