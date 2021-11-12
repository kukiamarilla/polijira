from django.db import models


class BurndownChart(models.Model):
    """
    BurndownChart Modela un Burndown Chart

    Args:
        models (Model): Model del módulo django
    Atributes:
        x (IntegerField): Horas de trabajo
        y (IntegerField): Dias de trabajo
    """
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
