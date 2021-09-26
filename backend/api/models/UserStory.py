from django.db import models
import datetime

ESTADOS = (
    ("P", "Pendiente"),
    ("R", "Release"),
    ("C", "Cancelado")
)

ESTADOS_ESTIMADOS = (
    ("N", "No estimado"),
    ("P", "Parcial"),
    ("C", "Completo")
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
    fecha_release = models.DateField(null=True)
    fecha_creacion = models.DateField()
    desarrollador = models.ForeignKey("Miembro", on_delete=models.CASCADE, related_name="user_stories", null=True)
    estado_estimacion = models.CharField(max_length=1, choices=ESTADOS_ESTIMADOS)
    product_backlog = models.BooleanField(default=False)

    def lanzar(self):
        """
        lanzar Libera este User Story
        """
        self.estado = "R"
        self.fecha_release = datetime.date.today()
        self.save()

    def cancelar(self):
        """
        cancelar Cancela este User Story
        """
        self.estado = "C"
        self.save()

    @staticmethod
    def create(
        nombre=None, descripcion=None, horas_estimadas=None, prioridad=None, estado_estimacion=None, autor=None,
        product_backlog_handler=None, registro_handler=None
    ):
        user_story = UserStory.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            horas_estimadas=horas_estimadas,
            prioridad=prioridad,
            estado_estimacion=estado_estimacion,
            fecha_creacion=datetime.date.today()
        )
        product_backlog_handler(user_story, autor.proyecto)
        registro_handler(user_story, autor)
        return user_story

    def update(
        self, nombre=None, descripcion=None, horas_estimadas=None, prioridad=None, estado_estimacion=None, autor=None,
        registro_handler=None
    ):
        self.nombre = nombre if nombre is not None else self.nombre
        self.descripcion = descripcion if descripcion is not None else self.descripcion
        self.horas_estimadas = horas_estimadas if horas_estimadas is not None else self.horas_estimadas
        self.prioridad = prioridad if prioridad is not None else self.prioridad
        self.estado_estimacion = estado_estimacion if estado_estimacion is not None else self.estado_estimacion
        self.save()
        registro_handler(self, autor)

    def asignar_desarrollador(self, desarrollador):
        self.desarrollador = desarrollador
        self.save()
