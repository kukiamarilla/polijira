from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from backend.api.models import Miembro, Sprint, Usuario, Proyecto, Review
from backend.api.serializers import SprintBacklogSerializer, SprintSerializer, ReviewSerializer
from backend.api.decorators import FormValidator
from backend.api.forms import CreateSprintForm, UpdateSprintForm


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
        """
        try:
            usuario_request = Usuario.objects.get(user=request.user)
            review = Review.objects.get(pk=pk)
            miembro = Miembro.objects.get(usuario=usuario_request, proyecto=review.user_story.proyecto)
            if not miembro.tiene_permiso("ver_user_stories"):
                response = {
                    "message": "No tiene permiso para realizar esta acción",
                    "permission_required": ["ver_user_stories"]
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            reviews = Review.objects.get(pk=pk)
            serializer = ReviewSerializer(reviews, many=False)
            return Response(serializer.data)
        except Review.DoesNotExist:
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
