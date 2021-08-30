from django.db import models


class Proyecto(models.Model):
    """
    Proyecto Modela la clase Proyecto

    Atributos:
        nombre {CharField} -- Nombre del proyecto
        fecha_inicio {DateField}  -- Fecha en que inicia el proyecto
        fecha_fin {DateField} -- Fecha en que termina el proyecto
        ESTADO  {choices} -- Indica los diferentes estados del proyecto
        estado {CharField} -- Indica el estado del proyecto
    """
    nombre = models.CharField(max_length=255, default='')
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    ESTADO = (('A', 'Activo'), ('F', 'Finalizado'), ('P', 'Pendiente'), ('C', 'Cancelado'))
    estado = models.CharField(max_length=1, choices=ESTADO, default='P')

    def iniciar(self):
        """
        iniciar Inicia este Proyecto
        """
        self.estado = 'A'
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
