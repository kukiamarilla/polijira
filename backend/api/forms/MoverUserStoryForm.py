from django.core.exceptions import ValidationError
from django import forms


class MoverUserStoryForm(forms.Form):
    """
    MoverUserStoryForm Valida los datos de request.data al cambiar el estado de un user story en el kanban

    Args:
        forms (Form): Form de django

    Atributes:
        estado_kanban (CharField): Campo para validar que el estado de kanban sea válido
    """

    estado_kanban = forms.CharField(
        max_length=1,
        required=True,
        error_messages={
            "required": "No especificaste el estado del kanban"
        }
    )

    def clean_estado_kanban(self):
        cleaned_data = super().clean()
        estado = cleaned_data.get("estado_kanban")
        if not estado == 'T' and not estado == 'D' and not estado == 'N':
            raise ValidationError("Estado Kanban no válido")
        return estado
