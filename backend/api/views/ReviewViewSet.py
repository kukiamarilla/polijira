from rest_framework import viewsets, status
from rest_framework.response import Response
from backend.api.models import Miembro, Usuario, Review, UserStory, SprintBacklog
from backend.api.serializers import ReviewSerializer
from backend.api.decorators import FormValidator
from backend.api.forms import CreateReviewForm, UpdateReviewForm
import datetime
from django.db import transaction


class ReviewViewSet(viewsets.ViewSet):
    """
    ReviewViewSet
    View para el modelo Review

    Args:
        viewsets (ViewSet): View del módulo rest_framework
    """

    def retrieve(self, request, pk=None):
        """
        retrieve
        Obtiene un review especificado

        Args:
            request (Any): request
            pk (int, optional): Primary key. Defaults to None.

        Returns:
            JSON: Review obtenido
        """
        try:
            usuario_request = Usuario.objects.get(user=request.user)
            review = Review.objects.get(pk=pk)
            miembro = Miembro.objects.get(usuario=usuario_request, proyecto=review.user_story.proyecto)
            if not miembro.tiene_permiso("ver_user_stories"):
                response = {
                    "message": "No tiene permiso para realizar esta acción",
                    "permission_required": ["ver_user_stories"],
                    "error": "forbidden"
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            reviews = Review.objects.get(pk=pk)
            serializer = ReviewSerializer(reviews, many=False)
            return Response(serializer.data)
        except Review.DoesNotExist:
            response = {
                "message": "No existe review del User Story",
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
    @FormValidator(form=CreateReviewForm)
    def create(self, request):
        """
        create
        Crea un review para un user story

        Args:
            request (Any): request

        Returns:
            JSON: Review creado
        """
        try:
            usuario_request = Usuario.objects.get(user=request.user)
            user_story = UserStory.objects.get(pk=request.data["user_story"])
            miembro = Miembro.objects.get(usuario=usuario_request, proyecto=user_story.proyecto)
            if not miembro.tiene_permiso("ver_user_stories") or not miembro.tiene_permiso("crear_reviews"):
                response = {
                    "message": "No tiene permiso para realizar esta acción",
                    "permission_required": [
                        "ver_user_stories",
                        "crear_reviews"
                    ],
                    "error": "forbidden"
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            if not user_story.estado == 'P':
                response = {
                    "message": "No se puede crear review en el estado actual del User Story",
                    "error": "forbidden"
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            sprint_backlog = SprintBacklog.objects.filter(user_story=user_story, sprint__estado="A")
            if not len(sprint_backlog):
                response = {
                    "message": "No se puede crear review si el user story no está en un sprint activo",
                    "error": "forbidden"
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            observacion = request.data["observacion"]
            review = Review.objects.create(
                user_story=user_story,
                observacion=observacion,
                fecha_creacion=datetime.date.today(),
                autor=usuario_request
            )
            serializer = ReviewSerializer(review, many=False)
            return Response(serializer.data)
        except Miembro.DoesNotExist:
            response = {
                "message": "Usted no es miembro de este Proyecto",
                "error": "forbidden"
            }
            return Response(response, status=status.HTTP_403_FORBIDDEN)

    @transaction.atomic
    @FormValidator(form=UpdateReviewForm)
    def update(self, request, pk=None):
        """
        update
        Modificar un review

        Args:
            request (Any): request
            pk (int, optional): Primary key. Defaults to None.

        Returns:
            JSON: Detalles del review modificado
        """
        try:
            usuario_request = Usuario.objects.get(user=request.user)
            review = Review.objects.get(pk=pk)
            miembro_request = Miembro.objects.get(
                usuario=usuario_request, proyecto=review.user_story.proyecto)
            if not usuario_request == review.autor:
                response = {
                    "message": "Usted no el autor de este review",
                    "error": "forbidden"
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            if not miembro_request.tiene_permiso("ver_user_stories") or \
               not miembro_request.tiene_permiso("modificar_reviews"):
                response = {
                    "message": "No tiene permiso para realizar esta acción",
                    "permission_required": [
                        "ver_user_stories",
                        "modificar_reviews"
                    ],
                    "error": "forbidden"
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            if not review.user_story.estado == 'P':
                response = {
                    "message": "No se puede modificar review en el estado actual del User Story",
                    "error": "forbidden"
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            sprint_backlog = SprintBacklog.objects.filter(user_story=review.user_story, sprint__estado="A")
            if not len(sprint_backlog):
                response = {
                    "message": "No se puede modificar review si el user story no está en un sprint activo",
                    "error": "forbidden"
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            review.observacion = request.data["observacion"]
            review.save()
            serializer = ReviewSerializer(review, many=False)
            return Response(serializer.data)
        except Review.DoesNotExist:
            response = {
                "message": "No existe el review especificado",
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
        destroy
        Elimina un review especificado

        Args:
            request (Any): request
            pk (int, optional): Primary key. Defaults to None.
        """
        try:
            usuario_request = Usuario.objects.get(user=request.user)
            review = Review.objects.get(pk=pk)
            miembro_request = Miembro.objects.get(
                usuario=usuario_request, proyecto=review.user_story.proyecto)
            if not usuario_request == review.autor:
                response = {
                    "message": "Usted no el autor de este review",
                    "error": "forbidden"
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            if not miembro_request.tiene_permiso("ver_user_stories") or \
                    not miembro_request.tiene_permiso("eliminar_reviews"):
                response = {
                    "message": "No tiene permiso para realizar esta acción",
                    "permission_required": [
                        "ver_user_stories",
                        "eliminar_reviews"
                    ],
                    "error": "forbidden"
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            if not review.user_story.estado == 'P':
                response = {
                    "message": "No se puede eliminar review en el estado actual del User Story",
                    "error": "forbidden"
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            sprint_backlog = SprintBacklog.objects.filter(user_story=review.user_story, sprint__estado="A")
            if not len(sprint_backlog):
                response = {
                    "message": "No se puede eliminar review si el user story no está en un sprint activo",
                    "error": "forbidden"
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            review.delete()
            response = {"message": "Review eliminado"}
            return Response(response)
        except Review.DoesNotExist:
            response = {
                "message": "No existe el review especificado",
                "error": "not_found"
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Miembro.DoesNotExist:
            response = {
                "message": "Usted no es miembro de este Proyecto",
                "error": "forbidden"
            }
            return Response(response, status=status.HTTP_403_FORBIDDEN)
