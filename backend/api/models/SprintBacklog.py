from django.db import models

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
    """
    sprint = models.ForeignKey("Sprint", on_delete=models.CASCADE, related_name="sprint_backlogs")
    user_story = models.ForeignKey("UserStory", on_delete=models.CASCADE, related_name="sprint_backlogs")
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

    def update(self, horas_estimadas=None, estado_estimacion=None):
        self.horas_estimadas = horas_estimadas if horas_estimadas is not None else self.horas_estimadas
        self.estado_estimacion = estado_estimacion if estado_estimacion is not None else self.estado_estimacion
        self.save()
