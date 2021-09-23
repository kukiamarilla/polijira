from django.db import models

ESTADOS = (
    ("P", "Pendiente"),
    ("R", "Release"),
    ("C", "Cancelado")
)


class UserStory(models.Model):
    """
    UserStory Modela la clase User Story

    Args:
        models (Model): Modelo de Django

    Atributes:
        nombre (CharField): Nombre del User Story
        descripcion (TextField): Descripcion del User Story
        horas_estimadas (IntegerField): Hora estimada del User Story
        prioridad (IntegerField): Prioridad del User Story
        estado (CharField): Estado actual de User Story
        fecha_release (DateField): Fecha en que se libera el User Story
        fecha_creacion (DateField): Fecha en que se crea el User Story
        desarrollador (ForeignKey): Miembro desarrollador del User Story
        estado_estimacion (CharField): Estado que se estima que tenga el User Story
        product_backlog (BooleanField): Atributo para saber si el User Story se encuentra en el Product Backlog
    """
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    horas_estimadas = models.IntegerField()
    prioridad = models.IntegerField()
    estado = models.CharField(max_length=1, choices=ESTADOS, default="P")
    fecha_release = models.DateField()
    fecha_creacion = models.DateField()
    desarrollador = models.ForeignKey("Miembro", on_delete=models.CASCADE, related_name="user_stories")
    estado_estimacion = models.CharField(max_length=1)
    product_backlog = models.BooleanField()

    def lanzar(self):
        """
        lanzar Libera este User Story
        """
        self.estado = "R"
        self.save()

    def cancelar(self):
        """
        cancelar Cancela este User Story
        """
        self.estado = "C"
        self.save()
