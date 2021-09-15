from backend.api.models.Proyecto import Proyecto
from django import forms
from django.core.exceptions import ValidationError
from backend.api.models import PermisoProyecto
import json


class CreateRolProyectoForm(forms.Form):
    """
    CreateRolForm Form para validar la creacion de RolProyecto

    Args:
        forms (Form): Form de django

    Atributes:
        nombre (CharField): Campo para validar el nombre de RolProyecto

        permisos (CharField): Campo para validar los permisos de RolProyecto

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
    proyecto = forms.CharField(
        required=True,
        error_messages={
            "required": "Se debe especificar un proyecto"
        }
    )

    def clean_permisos(self):
        """
        clean_permisos Valida los permisos a ser agregados a RolProyecto

        Raises:
            ValidationError: Error de validacion si no se encuentra el permiso

        Returns:
            JSON: Todos los permisos de proyecto correctamente validados
        """
        try:
            cleaned_data = super().clean()
            permisos = cleaned_data.get("permisos")
            permisos = permisos.replace("\'", "\"").replace("True", "true").replace("False", "false")
            permisos = json.loads(permisos)
            for permiso in permisos:
                PermisoProyecto.objects.get(pk=permiso["id"])
            return permisos
        except PermisoProyecto.DoesNotExist:
            raise ValidationError("No se encontró algunos de los permisos especificados")

    def clean_proyecto(self):
        try:
            cleaned_data = super().clean()
            proyecto = cleaned_data.get("proyecto")
            proyecto = Proyecto.objects.get(pk=proyecto)
            return proyecto
        except Proyecto.DoesNotExist:
            raise ValidationError("No se encontró el proyecto especificado")
