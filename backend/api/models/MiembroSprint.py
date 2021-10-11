from django.db import models


class MiembroSprint(models.Model):
    """
    MiembroSprint Modela un miembro de un Sprint

    Args:
        models (Model): Modelo de base de datos del módulo de django
    """

    miembro_proyecto = models.ForeignKey("Miembro", on_delete=models.CASCADE, related_name="miembro_sprints")
    sprint = models.ForeignKey("Sprint", on_delete=models.CASCADE, related_name="miembro_sprints")

    @staticmethod
    def pertenece_a_sprint_activo(usuario):
        """
        pertenece_a_sprint_activo Verifica si un usuario pertenece a un Sprint Activo

        Args:
            usuario (Usuario): Usuario a verificar
        """
        miembro_sprints = MiembroSprint.objects.filter(miembro_proyecto__usuario=usuario)
        for miembro_sprint in miembro_sprints:
            if miembro_sprint.sprint.estado == "A":
                return True
        return False
