from django.db import models

ESTADO = (
    ("P", "Pendiente"),
    ("A", "Activo"),
    ("F", "Finalizado")
)

ESTADOS_ESTIMADOS = (
    ("N", "No estimado"),
    ("P", "Parcial"),
    ("C", "Completo")
)


class Sprint(models.Model):
    """
    Sprint Modela un Sprint

    Args:
        models (Model): Modelo del módulo django

    Atributes:
        numero (IntegerField): Numeración automática
        fecha_inicio (DateField): Fecha estimada de inicio
        fecha_fin (DateField): Fecha estimada de fin
        estado (CharField): Estado actual que tiene el Sprint
        capacidad (IntegerField): Capacidad total en horas
        estado_sprint_planning (CharField): Estado actual del Sprint Planning
        planificador (ForeignKey): Miembro que planifica el Sprint
    """
    numero = models.IntegerField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    estado = models.CharField(max_length=1, choices=ESTADO, default="P")
    capacidad = models.IntegerField(default=0)
    estado_sprint_planning = models.CharField(max_length=1, choices=ESTADOS_ESTIMADOS, null=True)
    planificador = models.ForeignKey("Miembro", on_delete=models.CASCADE, related_name="sprints")

    def iniciar(self):
        """
        iniciar Inicia este Sprint
        """
        self.estado = "A"
        self.save()

    def finalizar(self):
        """
        finalizar Finaliza este Srpint
        """
        self.estado = "F"
        self.save()

    def _capacidad(self):
        """
        capacidad Retorna la capacidad de este Sprint
        """
        return self.capacidad
