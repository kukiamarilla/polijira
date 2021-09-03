from django.db import models


class Proyecto(models.Model):
    """
    Proyecto Modela la clase Proyecto

    Atributos:
        nombre {CharField} -- Nombre del proyecto
        fecha_inicio {DateField}  -- Fecha en que inicia el proyecto
        fecha_fin {DateField} -- Fecha en que termina el proyecto
        ESTADO  {choices} -- Diferentes estados del proyecto
        estado {CharField} -- Estado del proyecto
        scrum_master {ForeignKey} -- Scrum Master del proyecto
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
