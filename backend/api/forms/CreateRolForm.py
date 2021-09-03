from django import forms
from django.core.exceptions import ValidationError
from django.db import transaction
from backend.api.models import Permiso
import json


class CreateRolForm(forms.Form):
    nombre = forms.CharField(
        max_length=255,
        required=True,
        error_messages={
            "required": "No se especificó ningun nombre",
            "max_length": "El nombre superó el máximo número de caracteres"
        }
    )
    permisos = forms.CharField(
        required=True,
        error_messages={
            "required": "Se debe especificar al menos un permiso"
        }
    )

    @transaction.atomic
    def clean_permisos(self):
        try:
            cleaned_data = super().clean()
            permisos = json.loads(cleaned_data.get("permisos").replace("\'", "\""))
            for permiso in permisos:
                Permiso.objects.get(pk=permiso["id"])
            return permisos
        except Permiso.DoesNotExist:
            transaction.set_rollback(True)
            raise ValidationError("No se encontró algunos de los permisos especificados")
