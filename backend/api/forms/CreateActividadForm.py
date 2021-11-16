from django import forms
from django.core.exceptions import ValidationError
from backend.api.models import SprintBacklog


class CreateActividadForm(forms.Form):
    """
    CreateActividadForm Valida los datos enviados al Crear una Actividad

    Args:
        forms (Form): Form del módulo django
    """
    titulo = forms.CharField(
        error_messages={
            "required": "No se pasó: Título"
        }
    )
    sprint_backlog = forms.IntegerField(
        error_messages={
            "required": "No se pasó: Sprint Backlog"
        }
    )
    descripcion = forms.CharField(
        error_messages={
            "required": "No se pasó: Descripcion"
        }
    )
    horas = forms.IntegerField(
        min_value=0,
        required=True,
        error_messages={
            "required": "No se pasó: Horas",
            "min_value": "La hora no puede ser negativa"
        }
    )

    def clean_sprint_backlog(self):
        """
        clean_sprint_backlog Valida que el Sprint Backlog exista en la base de datos
        """
        try:
            cleaned_data = super().clean()
            id = cleaned_data.get("sprint_backlog")
            if id is None:
                raise ValidationError("Ocurrió un error inesperado para enviar el Sprint Backlog")
            SprintBacklog.objects.get(pk=id)
            return id
        except SprintBacklog.DoesNotExist:
            raise ValidationError("No se encontró el Sprint Backlog en la base de datos")
