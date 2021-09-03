from django import forms
from django.core.exceptions import ValidationError
from backend.api.models import Permiso


class AgregarPermisoRolForm(forms.Form):
    id = forms.IntegerField(
        required=True,
        error_messages={
            "required": "No se pasó ninguna id de Permiso"
        }
    )

    def clean_id(self):
        cleaned_data = super().clean()
        id = cleaned_data.get("id")
        try:
            Permiso.objects.get(pk=id)
        except Permiso.DoesNotExist:
            raise ValidationError("No existe el permiso en la base de datos")
