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

    @staticmethod
    def create(nombre=None, fecha_inicio=None, fecha_fin=None,
               scrum_master=None, roles_handler=None, scrum_master_handler=None
               ):
        """
        create Crea este Proyecto

        Args:
            nombre (String, optional): Nombre del Proyecto.
            fecha_inicio (String, optional): Fecha estimada de inicio.
            fecha_fin (String, optional): Fecha estimada de fin.
            scrum_master (Usuario, optional): Scrum Master del proyecto.
            roles_handler (method, optional): Asigna los roles por defecto a este proyecto.
            scrum_master_handler (method, optional): Asigna como miembro del proyecto al scrum master

        Returns:
            Proyecto: El proyecto con sus roles y miembros definidos
        """
        proyecto = Proyecto.objects.create(
            nombre=nombre,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            estado="P"
        )
        roles_handler(proyecto)
        scrum_master_handler(proyecto, scrum_master)
        return proyecto

    def update(self, nombre=None, fecha_inicio=None, fecha_fin=None, scrum_master=None, scrum_master_handler=None):
        """
        update Modifica este proyecto

        Args:
            nombre (String, optional): Nombre del Proyecto.
            fecha_inicio (String, optional): Fecha estimada de inicio.
            fecha_fin (String, optional): Fecha estimada de fin.
            scrum_master (Usuario, optional): Scrum Master del proyecto.
            scrum_master_handler (method, optional): Actualiza el miembro del proyecto si hay nuevo scrum master
        """
        self.nombre = nombre if nombre is not None else self.nombre
        self.fecha_inicio = fecha_inicio if fecha_inicio is not None else self.fecha_inicio
        self.fecha_fin = fecha_fin if fecha_inicio is not None else self.fecha_fin
        self.save()
        if scrum_master_handler is not None:
            scrum_master_handler(self, scrum_master)
        else:
            self.scrum_master = scrum_master if scrum_master is not None else self.scrum_master
            self.save()

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
        self.fecha_fin = str(date.today())
        self.save()

    def cancelar(self):
        """
        cancelar Cancela este Proyecto
        """
        self.estado = 'C'
        self.save()
