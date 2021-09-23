from django.db import models

ESTADOS = (
    ("P", "Pendiente"),
    ("R", "Release"),
    ("C", "Cancelado")
)


class UserStory(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    horas_estimadas = models.IntegerField()
    prioridad = models.IntegerField()
    estado = models.CharField(max_length=1, choices=ESTADOS, default="P")
    fecha_release = models.DateField()
    fecha_creacion = models.DateField()
    desarrollador = models.ForeignKey("Miembro", on_delete=models.CASCADE)
    estado_estimacion = models.CharField(max_length=1)
    product_backlog = models.BooleanField()

    def lanzar(self):
        self.estado = "R"
        self.save()

    def cancelar(self):
        self.estado = "C"
        self.save()
