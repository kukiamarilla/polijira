from django import forms
from django.core.exceptions import ValidationError
from backend.api.models import Permiso, PlantillaRolProyecto
import json


class CreatePlantillaRolProyectoForm(forms.Form):
    """
    CreateRolForm Form para validar la creacion de PlantillaRolProyecto

    Args:
        forms (Form): Form de django

    Atributes:
        nombre (CharField): Campo para validar el nombre de PlantillaRolProyecto

        permisos (CharField): Campo para validar los permisos de PlantillaRolProyecto

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
        clean_permisos Valida los permisos a ser agregados a PlantillaRolProyecto

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
                Permiso.objects.get(pk=permiso["id"])
            return permisos
        except Permiso.DoesNotExist:
            raise ValidationError("No se encontró algunos de los permisos especificados")

    def clean_nombre(self):
        """
        clean_nombre Valida que no se cree dos plantillas con el mismo nombre

        Raises:
            ValidationError: Error de validación

        Returns:
            str: Nombre de la plantilla
        """
        try:
            cleaned_data = super().clean()
            nombre = cleaned_data.get("nombre")
            PlantillaRolProyecto.objects.get(nombre=nombre)
            raise ValidationError("No puede existir dos plantillas con el mismo nombre")
        except PlantillaRolProyecto.DoesNotExist:
            return nombre
