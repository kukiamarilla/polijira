from django.db import models


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
