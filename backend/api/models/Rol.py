from django.db import models
from .Permiso import Permiso


class Rol(models.Model):
    """
    Modela la clase Rol

    Atributos:
        nombre {str} -- Nombre del rol
        permisos {Permiso[]} -- Permisos del rol
    """

    nombre = models.CharField(max_length=255, default="")
    permisos = models.ManyToManyField(Permiso)

    def agregar_permiso(self, permiso):
        """
        agregar_permiso Agrega un permiso al rol de sistema

        Args:
            permiso (Permiso): Permiso a agregar
        """
        self.permisos.add(permiso)

    def eliminar_permiso(self, permiso):
        """
        eliminar_permiso Elimina un permiso de rol de sistema

        Args:
            permiso (Permiso): Permiso a eliminar
        """
        self.permisos.remove(permiso)
