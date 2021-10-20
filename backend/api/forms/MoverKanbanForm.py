from django.core.exceptions import ValidationError
from backend.api.models import UserStory
from django import forms


class MoverKanbanForm(forms.Form):
    """
    MoverKanbanForm Valida los datos de request.data al cambiar el estado de un user story en el kanban

    Args:
        forms (Form): Form de django

    Atributes:
        user_story (IntegerField): Campo para validar que exista el user story
        estado_kanban (CharField): Campo para validar que el estado de kanban sea válido
    """
    user_story = forms.IntegerField(
        min_value=1,
        required=True,
        error_messages={
            "required": "No especificaste el user story"
        }
    )

    estado_kanban = forms.CharField(
        max_length=1,
        required=True,
        error_messages={
            "required": "No especificaste el estado del kanban"
        }
    )

    def clean_user_story(self):
        """
        clean_user_story [summary]

        Raises:
            ValidationError: [description]

        Returns:
            [type]: [description]
        """
        try:
            cleaned_data = super().clean()
            id = cleaned_data.get("user_story")
            UserStory.objects.get(pk=id)
            return id
        except UserStory.DoesNotExist:
            raise ValidationError("No se encontró un user story en la base de datos")

    def clean_estado_kanban(self):
        cleaned_data = super().clean()
        estado = cleaned_data.get("estado_kanban")
        if not (estado == 'T' or estado == 'D' or estado == 'N'):
            raise ValidationError("Estado Kanban no válido")
        return estado
