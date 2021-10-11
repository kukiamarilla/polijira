from django.db import models

ESTADOS_SPRINT = (
    ("P", "Pendiente"),
    ("A", "Activo"),
    ("F", "Finalizado")
)

ESTADOS_SPRINT_PLANNING = (
    ("I", "Iniciado"),
    ("F", "Finalizado"),
    ("P", "Pendiente")
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
        proyecto (ForeignKey): Proyecto al que pertenece el Sprint
    """
    numero = models.IntegerField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    estado = models.CharField(max_length=1, choices=ESTADOS_SPRINT, default="P")
    capacidad = models.IntegerField(default=0)
    estado_sprint_planning = models.CharField(max_length=1, choices=ESTADOS_SPRINT_PLANNING, default="P")
    planificador = models.ForeignKey("Miembro", on_delete=models.CASCADE, related_name="sprints", null=True)
    proyecto = models.ForeignKey("Proyecto", on_delete=models.CASCADE, related_name="sprints", null=True)

    @staticmethod
    def create(fecha_inicio=None, fecha_fin=None, capacidad=None, proyecto=None):
        """
        create Crea un Sprint

        Args:
            fecha_inicio (str): Fecha estimada de inicio del Sprint
            fecha_fin (str): Fecha estimada de fin del Sprint
            capacidad (int): Capacidad total en horas del Sprint
            proyecto (Proyecto): Proyecto al que pertenece el Sprint

        Returns:
            Sprint: El Sprint con los parametros enviados
        """
        numeracion = Sprint.objects.filter(proyecto=proyecto).count() + 1
        sprint = Sprint.objects.create(
            numero=numeracion,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            capacidad=capacidad,
            proyecto_id=proyecto
        )
        return sprint

    def update(self, fecha_inicio=None, fecha_fin=None):
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.save()

    def activar(self):
        """
        iniciar Activa este Sprint
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

    def iniciar_sprint_planning(self):
        """
        iniciar_sprint_planning Inicia el Sprint Planning
        """
        self.estado_sprint_planning = "I"
        self.save()

    @staticmethod
    def se_solapa(proyecto=None, fecha_inicio=None, fecha_fin=None):
        sprints = Sprint.objects.filter(proyecto=proyecto).exclude(estado="F")
        for sprint in sprints:
            if (fecha_inicio >= str(sprint.fecha_inicio) and fecha_fin <= str(sprint.fecha_fin)) or \
               (fecha_inicio < str(sprint.fecha_inicio) and fecha_fin >= str(sprint.fecha_inicio)) or \
               (fecha_inicio <= str(sprint.fecha_fin) and fecha_fin > str(sprint.fecha_fin)):
                return True
        return False
