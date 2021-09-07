from django.db import models


class PermisoProyecto(models.Model):
    """
    PermisoProyecto Modela los permisos de proyecto

    Args:
        models (Model): Modelo de Django

    Arguments:
        nombre (CharField): Nombre del permiso
        codigo (CharField): Codigo del permiso
    """
    nombre = models.CharField(max_length=255, default="")
    codigo = models.CharField(max_length=255, default="")
