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
    def agregar_user_story(sprint=None, user_story=None):
        SprintBacklog.objects.create(sprint=sprint, user_story=user_story)
