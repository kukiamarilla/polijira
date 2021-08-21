from django.db import models
from .Permiso import Permiso


class Rol(models.Model):
    """
    Modela la clase Rol

    Atributos:
        nombre {CharField} -- nombre del rol
    """

    nombre = models.CharField(max_length=255, default="")
    permisos = models.ManyToManyField(Permiso)
