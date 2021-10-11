from django import forms
from django.core.exceptions import ValidationError
from backend.api.models import Permiso, Rol
import json


class CreateRolForm(forms.Form):
    """
    CreateRolForm Form para la creacion de Rol

    Args:
        forms (Form): Form de django

    Atributes:
        nombre (CharField): Campo para validar el nombre de Rol

        permisos (CharField): Campo para validar los permisos de Rol

    Raises:
        ValidationError: Error de Validacion

    """
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

    def clean_permisos(self):
        """
        clean_permisos Valida los permisos agregados a Rol

        Raises:
            ValidationError: Error de validacion si no se encuentra el permiso

        Returns:
            Permisos[]: Lista de Permiso validado correctamente
        """
        try:
            cleaned_data = super().clean()
            permisos = cleaned_data.get("permisos")
            permisos = permisos.replace("\'", "\"").replace("True", "true").replace("False", "false")
            permisos = json.loads(permisos)
            for permiso in permisos:
                Permiso.objects.get(pk=permiso["id"])
            return permisos
        except Permiso.DoesNotExist:
            raise ValidationError("No se encontró algunos de los permisos especificados")

    def clean_nombre(self):
        """
        clean_nombre Valida que el nombre del rol sea único

        Raises:
            ValidationError: Error de validacion si no se encuentra el rol
        """
        cleaned_data = super().clean()
        nombre = cleaned_data.get("nombre")
        rol = Rol.objects.filter(nombre=nombre)
        if len(rol) > 0:
            raise ValidationError("Ya existe un rol con ese nombre")
        return nombre
