from django import forms
from django.core.exceptions import ValidationError
from backend.api.models import UserStory, Miembro


class PlanificarUserStoryForm(forms.Form):
    """
    PlanificarUserStoryForm Valida los datos al Planificar un User Story

    Args:
        forms (Form): Form del módulo Django
    """
    user_story = forms.IntegerField(
        error_messages={
            "required": "No se especificó ningún User Story"
        }
    )
    horas_estimadas = forms.IntegerField(
        min_value=0,
        error_messages={
            "required": "No se especificó ninguna hora estimada",
            "min_value": "La hora no puede ser negativa"
        }
    )
    desarrollador = forms.IntegerField(
        error_messages={
            "required": "No se especificó ningún desarrollador"
        }
    )

    def clean_user_story(self):
        try:
            cleaned_data = super().clean()
            id = cleaned_data.get("user_story")
            if id is None:
                raise ValidationError("Hubo problemas para recibir el User Story")
            UserStory.objects.get(pk=id)
            return id
        except UserStory.DoesNotExist:
            raise ValidationError("No se encontró un User Story en la base de datos")

    def clean_desarrollador(self):
        try:
            cleaned_data = super().clean()
            id = cleaned_data.get("desarrollador")
            if id is None:
                raise ValidationError("Hubo problemas para recibir el Desarrollador")
            Miembro.objects.get(pk=id)
            return id
        except Miembro.DoesNotExist:
            raise ValidationError("No se encontró un Miembro de Sprint en la base de datos")
