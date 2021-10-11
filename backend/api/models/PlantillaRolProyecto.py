from django.db import models


class PlantillaRolProyecto(models.Model):
    """
    PlantillaRolProyecto Modelo los roles de Proyecto en formato Plantilla

    Args:
        models (Model): Modelo de Django

    Atributes:
        nombre (CharField): Nombre del rol
        permisos (ManyToManyField): Permisos del rol
    """
    nombre = models.CharField(max_length=255, default="", unique=True)
    permisos = models.ManyToManyField('PermisoProyecto')

    def agregar_permiso(self, permiso):
        """
        agregar_permiso Agrega un permiso de proyecto a este rol

        Args:
            permiso (PermisoProyecto): Permiso de Proyecto
        """
        self.permisos.add(permiso)

    def eliminar_permiso(self, permiso):
        """
        eliminar_permiso Elimina un permiso de proyecto a este rol

        Args:
            permiso (PermisoProyecto): Permiso de Proyecto
        """
        self.permisos.remove(permiso)
