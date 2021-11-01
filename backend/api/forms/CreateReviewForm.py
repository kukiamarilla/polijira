from django.core.exceptions import ValidationError
from backend.api.models import UserStory
from django import forms


class CreateReviewForm(forms.Form):
    """
    CreateReviewForm Valida los datos del request.data al crear un review

    Args:
        forms (Form): Form de django

    Atributes:
        user_story (IntegerField): Campo para validar que exista el user story
        observacion (TextField): Campo para validar que se especifca la observacion
    """
    user_story = forms.IntegerField(
        min_value=1,
        required=True,
        error_messages={
            "required": "No especificaste el user story"
        }
    )

    observacion = forms.CharField(
        required=True,
        error_messages={
            "required": "No especificaste la observacion"
        }
    )

    def clean_user_story(self):
        """
        clean_user_story Valida que el id de user story exista en la BD

        Raises:
            ValidationError: Error de Validación

        Returns:
            int: id de user story
        """
        try:
            cleaned_data = super().clean()
            id = cleaned_data.get("user_story")
            UserStory.objects.get(pk=id)
            return id
        except UserStory.DoesNotExist:
            raise ValidationError("No se encontro el user story en la base de datos")
