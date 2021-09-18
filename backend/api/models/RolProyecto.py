from backend.api.models import PlantillaRolProyecto
from django.db import models


class RolProyecto(models.Model):
    """
    RolProyecto Modelo los roles de Proyecto

    Args:
        models (Model): Modelo de Django

    Atributos:
        nombre (CharField): Nombre del rol
        permisos (ManyToManyField): Permisos del rol
        proyecto (ForeignKey): Proyecto del rol
    """

    nombre = models.CharField(max_length=255, default="")
    permisos = models.ManyToManyField("PermisoProyecto")
    proyecto = models.ForeignKey("Proyecto", on_delete=models.CASCADE, related_name="roles")

    def agregar_permiso(self, permiso):
        """
        agregar_permiso Agrega un permiso de proyecto a este rol

        Args:
            permiso (Permiso Proyecto): Permiso de Proyecto
        """
        self.permisos.add(permiso)

    def eliminar_permiso(self, permiso):
        """
        eliminar_permiso Elimina un permiso de proyecto a este rol

        Args:
            permiso (PermisoProyecto): Permiso de Proyecto
        """
        self.permisos.remove(permiso)

    @staticmethod
    def from_plantilla(proyecto):
        """
        from_plantilla Crea los roles por defecto de un proyecto

        Args:
            proyecto (Proyecto): Proyecto a asignar los roles por defecto
        """
        plantillas = PlantillaRolProyecto.objects.all()
        for plantilla in plantillas:
            rol_proyecto = RolProyecto.objects.create(
                nombre=plantilla.nombre,
                proyecto=proyecto
            )
            rol_proyecto.permisos.set(plantilla.permisos.all())
