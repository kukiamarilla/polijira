from datetime import date
from django.db import models


class Proyecto(models.Model):
    """
    Proyecto Modela el Proyecto

    Args:
        models (Model): Modelo de Django

    Atributes:
        nombre (CharField): Nombre del Proyecto
        fecha_inicio (DateField): Fecha estimada de inicio
        fecha_fin (DateField): Fecha estimada de fin
        ESTADO (tuple): Definicion de diferentes estados que puede tener el Proyecto
        estado (CharField): Estado del Proyecto
        scrum_master (ForeignKey): Scrum Master del proyecto
    """
    nombre = models.CharField(max_length=255, default='')
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    ESTADO = (('A', 'Activo'), ('F', 'Finalizado'), ('P', 'Pendiente'), ('C', 'Cancelado'))
    estado = models.CharField(max_length=1, choices=ESTADO, default='P')
    scrum_master = models.ForeignKey('Usuario', on_delete=models.CASCADE,
                                     related_name='proyecto_scrum_master', null=True)

    def iniciar(self):
        """
        iniciar Inicia este Proyecto
        """
        self.estado = 'A'
        self.fecha_inicio = str(date.today())
        self.save()

    def finalizar(self):
        """
        finalizar Finaliza este Proyecto
        """
        self.estado = 'F'
        self.save()

    def cancelar(self):
        """
        cancelar Cancela este Proyecto
        """
        self.estado = 'C'
        self.save()
