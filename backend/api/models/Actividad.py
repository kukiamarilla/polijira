from django.db import models


class Actividad(models.Model):
    """
    Actividad Modela las actividades de un User Story

    Args:
        models (Model): Modelo del módulo Django
    """

    descripcion = models.TextField(default="")
    horas = models.IntegerField(default=0)
    fecha_creacion = models.DateField()
    sprint_backlog = models.ForeignKey("SprintBacklog", on_delete=models.CASCADE,
                                       related_name="actividades", null=True)
    desarrollador = models.ForeignKey("Usuario", on_delete=models.CASCADE, null=True)
