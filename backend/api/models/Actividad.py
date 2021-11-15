from django.db import models


class Actividad(models.Model):
    """
    Actividad Modela las actividades de un User Story

    Args:
        models (Model): Modelo del módulo Django
    """

    titulo = models.TextField(default="")
    descripcion = models.TextField(default="")
    horas = models.IntegerField(default=0)
    fecha_creacion = models.DateField()
    sprint_backlog = models.ForeignKey("SprintBacklog", on_delete=models.CASCADE,
                                       related_name="actividades", null=True)
    desarrollador = models.ForeignKey("Usuario", on_delete=models.CASCADE, null=True)

    def update(self, horas=None, descripcion=None, titulo=None):
        self.horas = horas if horas is not None else self.horas
        self.descripcion = descripcion if descripcion is not None else self.descripcion
        self.titulo = titulo if titulo is not None else self.titulo
        self.save()
