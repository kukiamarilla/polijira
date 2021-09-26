from django.db import transaction
from backend.api.forms import CreateUserStoryForm
from backend.api.serializers import UserStorySerializer
from rest_framework.response import Response
from backend.api.models import Miembro, ProductBacklog, RegistroUserStory, UserStory, Usuario
from rest_framework import viewsets, status
from backend.api.decorators import FormValidator


class UserStoryViewSet(viewsets.ViewSet):
    """
    UserStoryViewSet View para el modelo User Story

    Args:
        viewsets (ViewSet): View del módulo rest_framework
    """

    def retrieve(self, request, pk=None):
        """
        retrieve Obtiene los detalles de un User Story

        Args:
            request (Any): Request hecho por el usuario
            pk (int, optional): Primary key del User Story. Defaults to None.

        Returns:
            JSON: Detalles del User Story
        """
        try:
            usuario_request = Usuario.objects.get(user=request.user)
            user_story = UserStory.objects.get(pk=pk)
            miembro_request = Miembro.objects.get(
                usuario=usuario_request, proyecto=user_story.registro.autor.proyecto)
            if not miembro_request.tiene_permiso("ver_user_stories"):
                response = {
                    "message": "No tiene permiso para realizar esta acción",
                    "permission_required": ["ver_user_stories"],
                    "error": "forbidden"
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            serializer = UserStorySerializer(user_story, many=False)
            return Response(serializer.data)
        except UserStory.DoesNotExist:
            response = {
                "message": "No existe el User Story",
                "error": "not_found"
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

    @transaction.atomic
    @FormValidator(form=CreateUserStoryForm)
    def create(self, request):
        try:
            usuario_request = Usuario.objects.get(user=request.user)
            miembro_request = Miembro.objects.filter(usuario=usuario_request, proyecto_id=request.data["proyecto"])[0]
            if not miembro_request.tiene_permiso("crear_user_stories"):
                response = {
                    "message": "No tiene permiso para realizar esta acción",
                    "permission_required": ["crear_user_stories"],
                    "error": "forbidden"
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            user_story = UserStory.create(
                nombre=request.data["nombre"],
                descripcion=request.data["descripcion"],
                horas_estimadas=request.data["horas_estimadas"],
                prioridad=request.data["prioridad"],
                estado_estimacion=request.data["estado_estimacion"],
                autor=miembro_request,
                product_backlog_handler=ProductBacklog.almacenar_user_story,
                registro_handler=RegistroUserStory.crear_registro
            )
            # En el Sprint
            # if miembro_request.tiene_permiso("ver_miembros"):
            #     user_story.asignar_desarrollador(desarrollador)
            serializer = UserStorySerializer(user_story, many=False)
            return Response(serializer.data)
        except IndexError:
            response = {
                "message": "Usted no es miembro de este Proyecto",
                "error": "forbidden"
            }
            return Response(response, status=status.HTTP_403_FORBIDDEN)