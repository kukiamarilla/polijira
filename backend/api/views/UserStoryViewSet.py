from django.db import transaction
from backend.api.forms import CreateUserStoryForm, UpdateUserStoryForm
from backend.api.serializers import RegistroUserStorySerializer, UserStorySerializer
from rest_framework.response import Response
from backend.api.models import Miembro, ProductBacklog, RegistroUserStory, UserStory, Usuario
from rest_framework import viewsets, status
from backend.api.decorators import FormValidator
from rest_framework.decorators import action


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
                usuario=usuario_request, proyecto=user_story.registros.get(accion="Creacion").autor.proyecto)
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
            miembro_request = Miembro.objects.get(usuario=usuario_request, proyecto_id=request.data["proyecto"])
            if not miembro_request.tiene_permiso("crear_user_stories"):
                response = {
                    "message": "No tiene permiso para realizar esta acción",
                    "permission_required": ["crear_user_stories"],
                    "error": "forbidden"
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            user_story = UserStory.create(
                nombre=request.data.get("nombre"),
                proyecto=request.data.get("proyecto"),
                descripcion=request.data.get("descripcion") if request.data.get("descripcion") is not None else "",
                prioridad=request.data.get("prioridad") if request.data.get("prioridad") is not None else 0,
                autor=miembro_request,
                product_backlog_handler=ProductBacklog.almacenar_user_story,
                registro_handler=RegistroUserStory.crear_registro
            )
            # En el Sprint
            # if miembro_request.tiene_permiso("ver_miembros"):
            #     user_story.asignar_desarrollador(desarrollador)
            serializer = UserStorySerializer(user_story, many=False)
            return Response(serializer.data)
        except Miembro.DoesNotExist:
            response = {
                "message": "Usted no es miembro de este Proyecto",
                "error": "forbidden"
            }
            return Response(response, status=status.HTTP_403_FORBIDDEN)

    @transaction.atomic
    @FormValidator(form=UpdateUserStoryForm)
    def update(self, request, pk=None):
        try:
            usuario_request = Usuario.objects.get(user=request.user)
            user_story = UserStory.objects.get(pk=pk)
            miembro_request = Miembro.objects.get(
                usuario=usuario_request, proyecto=user_story.registros.get(accion="Creacion").autor.proyecto
            )
            if not miembro_request.tiene_permiso("ver_user_stories") or \
               not miembro_request.tiene_permiso("modificar_user_stories"):
                response = {
                    "message": "No tiene permiso para realizar esta acción",
                    "permission_required": ["ver_user_stories", "modificar_user_stories"],
                    "error": "forbidden"
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            if not user_story.estado == "P":
                response = {
                    "message": "Este User Story no tiene el estado Pendiente para ser modificado",
                    "error": "conflict"
                }
                return Response(response, status=status.HTTP_409_CONFLICT)
            user_story.update(
                nombre=request.data["nombre"],
                descripcion=request.data["descripcion"],
                prioridad=request.data["prioridad"],
                autor=miembro_request,
                registro_handler=RegistroUserStory.modificar_registro
            )
            serializer = UserStorySerializer(user_story, many=False)
            return Response(serializer.data)
        except UserStory.DoesNotExist:
            response = {
                "message": "No existe el User Story",
                "error": "not_found"
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Miembro.DoesNotExist:
            response = {
                "message": "Usted no es miembro de este Proyecto",
                "error": "forbidden"
            }
            return Response(response, status=status.HTTP_403_FORBIDDEN)

    @transaction.atomic
    def destroy(self, request, pk=None):
        try:
            usuario_request = Usuario.objects.get(user=request.user)
            user_story = UserStory.objects.get(pk=pk)
            miembro_request = Miembro.objects.get(
                usuario=usuario_request, proyecto=user_story.registros.get(accion="Creacion").autor.proyecto)
            if not miembro_request.tiene_permiso("ver_user_stories") or \
               not miembro_request.tiene_permiso("eliminar_user_stories"):
                response = {
                    "message": "No tiene permiso para realizar esta acción",
                    "permission_required": ["ver_user_stories", "eliminar_user_stories"],
                    "error": "forbidden"
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            if not user_story.product_backlog:
                response = {
                    "message": "Este User Story no se encuentra en el Product Backlog",
                    "error": "conflict"
                }
                return Response(response, status=status.HTTP_409_CONFLICT)
            user_story.delete(
                autor=miembro_request,
                registro_handler=RegistroUserStory.eliminar_registro,
                product_backlog_handler=ProductBacklog.eliminar_user_story
            )
            response = {
                "message": "User Story Eliminado"
            }
            return Response(response, status=status.HTTP_200_OK)
        except UserStory.DoesNotExist:
            response = {
                "message": "No existe el User Story",
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
    def registros(self, request, pk=None):
        try:
            usuario = Usuario.objects.get(user=request.user)
            user_story = UserStory.objects.get(pk=pk)
            miembro = Miembro.objects.get(
                usuario=usuario, proyecto=user_story.registros.get(accion="Creacion").autor.proyecto
            )
            if not miembro.tiene_permiso("ver_user_stories"):
                response = {
                    "message": "No tiene permiso para realizar esta acción",
                    "permission_required": ["ver_user_stories"],
                    "error": "forbidden"
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            registros = user_story.registros.all()
            serializer = RegistroUserStorySerializer(registros, many=True)
            return Response(serializer.data)
        except UserStory.DoesNotExist:
            response = {
                "message": "No existe el User Story",
                "error": "not_found"
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
