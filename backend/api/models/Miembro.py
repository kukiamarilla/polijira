from django.db import models
from backend.api.models import PermisoProyecto, RolProyecto


class Miembro(models.Model):
    """
    Miembro Modela el Miembro

    Args:
        models (Model): Modelo de Django

    Atributes:
        usuario (ForeignKey): Usuario relacionado con el miembro
        proyecto (ForeignKey): Proyecto en el que se encuentra el miembro
        rol (ForeignKey): Rol de proyecto del miembro en el proyecto
    """

    usuario = models.ForeignKey("Usuario", on_delete=models.CASCADE, related_name='miembros')
    proyecto = models.ForeignKey("Proyecto", on_delete=models.CASCADE, related_name='miembros')
    rol = models.ForeignKey("RolProyecto", on_delete=models.CASCADE, related_name='miembros')

    def tiene_permiso(self, permiso_codigo):
        """
        Comprueba si este miembro tiene el permiso de proyecto especificado

        Args:
            permiso_codigo (String): el codigo del permiso de proyecto

        Returns:
            bool: True, False
        """
        try:
            self.rol.permisos.get(codigo=permiso_codigo)
            return True
        except PermisoProyecto.DoesNotExist:
            return False

    @staticmethod
    def asignar_scrum_master(proyecto, scrum_master):
        """
        asignar_scrum_master Asigna un Scrum Master a un Proyecto

        Args:
            proyecto (Proyecto): Proyecto a asignar el scrum master
            scrum_master (Usuario): Scrum Master a ser asignado
        """
        proyecto.scrum_master = scrum_master
        proyecto.save()
        Miembro.objects.create(
            usuario=proyecto.scrum_master,
            proyecto=proyecto,
            rol=RolProyecto.objects.get(nombre="Scrum Master", proyecto=proyecto)
        )

    @staticmethod
    def actualizar_scrum_master(proyecto, scrum_master):
        """
        actualizar_scrum_master Actualiza un Scrum Master de un Proyecto

        Args:
            proyecto (Proyecto): Proyecto a actualizar el scrum master
            scrum_master (Usuario): Scrum Master a ser actualizado
        """
        rol = RolProyecto.objects.get(nombre="Scrum Master", proyecto=proyecto)
        miembro = Miembro.objects.get(
            usuario=proyecto.scrum_master,
            proyecto=proyecto,
            rol=rol
        )
        miembro.delete()
        proyecto.update(scrum_master=scrum_master)
        Miembro.objects.create(
            usuario=scrum_master,
            proyecto=proyecto,
            rol=rol
        )

    @staticmethod
    def es_miembro(usuario, proyecto):
        try:
            Miembro.objects.get(usuario=usuario, proyecto=proyecto)
            return True
        except Miembro.DoesNotExist:
            return False
