from django.db import models

ESTADOS_KANBAN = (
    ("T", "Todo"),
    ("D", "Doing"),
    ("N", "Done")
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
    estado_kanban = models.CharField(max_length=1, choices=ESTADOS_KANBAN, default="T")

    @staticmethod
    def agregar_user_story(sprint=None, user_story=None):
        SprintBacklog.objects.create(sprint=sprint, user_story=user_story)

    def mover_kanban(self, estado):
        """
        mover Mueve el user story a la siguiente columna del Kanban
        """
        self.estado_kanban = estado
        self.save()
