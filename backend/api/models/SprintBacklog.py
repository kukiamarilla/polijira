from django.db import models

ESTADOS_KANBAN = (
    ("T", "Todo"),
    ("D", "Doing"),
    ("N", "Done")
)

ESTADOS_ESTIMADOS = (
    ("N", "No estimado"),
    ("p", "Parcial"),
    ("C", "Completo"),
    ("P", "Pendiente")
)


class SprintBacklog(models.Model):
    """
    SprintBacklog Modela Sprint Backlog

    Args:
        models (Model): Modelo del módulo de django

    Atributes:
        sprint (ForeignKey): Sprint del que planifica este Sprint Backlog
        user_story (ForeignKey): User Story del desarrollador relacionado a este Sprint Backlog
        estado_kanban(CharField): Columna del kanban donde se encuentra el User Story
        horas_estimadas (ForeignKey): horas estimadas para el user story
        estado_estimacion(CharField): estado de estimacion en el que se encuentra un User Story
    """
    sprint = models.ForeignKey("Sprint", on_delete=models.CASCADE, related_name="sprint_backlogs")
    user_story = models.ForeignKey("UserStory", on_delete=models.CASCADE, related_name="sprint_backlogs")
    estado_kanban = models.CharField(max_length=1, choices=ESTADOS_KANBAN, default="T")
    desarrollador = models.ForeignKey("MiembroSprint", on_delete=models.CASCADE,
                                      related_name="sprint_backlogs", null=True)
    horas_estimadas = models.IntegerField(default=0)
    estado_estimacion = models.CharField(max_length=1, choices=ESTADOS_ESTIMADOS, default="P")

    @staticmethod
    def create(sprint=None, user_story=None, horas_estimadas=None, desarrollador=None):
        sprint_backlog = SprintBacklog.objects.create(
            sprint=sprint,
            user_story=user_story,
            desarrollador=desarrollador,
            horas_estimadas=horas_estimadas,
            estado_estimacion="p" if sprint.planificador is not None else "P"
        )
        return sprint_backlog

    def mover_kanban(self, estado):
        """
        mover Mueve el user story a la siguiente columna del Kanban
        """
        self.estado_kanban = estado
        self.save()

    def update(self, horas_estimadas=None, estado_estimacion=None):
        self.horas_estimadas = horas_estimadas if horas_estimadas is not None else self.horas_estimadas
        self.estado_estimacion = estado_estimacion if estado_estimacion is not None else self.estado_estimacion
        self.save()

    def devolver_al_product_backlog(self, product_backlog_handler=None):
        product_backlog_handler(self.user_story, self.sprint.proyecto)
        self.delete()
