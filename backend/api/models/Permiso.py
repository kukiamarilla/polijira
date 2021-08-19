from django.db import models


class Permiso(models.Model):
    """
    Modela la clase Permiso

    Atributos:
        nombre {CharField} -- nombre del permiso
        codigo {CharField}  -- código del permiso
    """

    nombre = models.CharField(max_length=255, default="")
    codigo = models.CharField(max_length=255, default="")
