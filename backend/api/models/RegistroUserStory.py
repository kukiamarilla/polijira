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


class RegistroUserStory(models.Model):
    """
    RegistroUserStory Modela la clase Registro de User Stories

    Args:
        models (Model): Modelo de django

    Atributes:
        nombre_antes (CharField): Nombre que toma el registro si se realiza una modificación o eliminación
        descripcion_antes (TextField): Descripcion que toma el registro si se realiza una modificación o eliminación
        hora_estimada_antes (IntegerField): Hora estimada que toma el registro si se realiza una modificación o eliminación
        prioridad_antes (IntegerField): Prioridad que toma el registro si se realiza una modificación o eliminación
        estado_antes (CharField): Estado que toma el registro si se realiza una modificación o eliminación
        desarrollador_antes (ForeignKey): Desarrollador que toma el registro si se realiza una modificación o eliminación
        nombre_despues (CharField): Nombre que toma el registro si se realiza una creación o modificación
        descripcion_despues (TextField): Descripcion que toma el registro si se realiza una creación o modificación
        hora_estimada_despues (IntegerField): Hora estimada que toma el registro si se realiza una creación o modificación
        prioridad_despues (IntegerField): Prioridad que toma el registro si se realiza una creación o modificación
        estado_despues (CharField): Estado que toma el registro si se realiza una creación o modificación
        desarrollador_despues (ForeignKey): Desarrollador que toma el registro si se realiza una creación o modificación
        user_story (OneToOneField): User Story que se registra
        accion (CharField): Indica si se realizo una creación, modificación o eliminación
        autor (ForeignKey): Miembro que realiza el registro
    """
    nombre_antes = models.CharField(max_length=255, null=True)
    descripcion_antes = models.TextField(null=True)
    horas_estimadas_antes = models.IntegerField(null=True)
    prioridad_antes = models.IntegerField(null=True)
    estado_antes = models.CharField(max_length=1, choices=ESTADOS, null=True)
    desarrollador_antes = models.ForeignKey("Miembro", on_delete=models.CASCADE,
                                            related_name="registro_user_stories_antes", null=True)
    nombre_despues = models.CharField(max_length=255)
    descripcion_despues = models.TextField()
    horas_estimadas_despues = models.IntegerField()
    prioridad_despues = models.IntegerField()
    estado_despues = models.CharField(max_length=1, choices=ESTADOS)
    desarrollador_despues = models.ForeignKey(
        "Miembro", on_delete=models.CASCADE, related_name="registro_user_stories_despues", null=True)
    user_story = models.OneToOneField("UserStory", on_delete=models.CASCADE, related_name="registro_user_stories")
    accion = models.CharField(max_length=50)
    fecha = models.DateField()
    autor = models.ForeignKey("Miembro", on_delete=models.CASCADE, related_name="registro_user_stories")

    @staticmethod
    def crear_registro(user_story, autor):
        RegistroUserStory.objects.create(
            nombre_despues=user_story.nombre,
            descripcion_despues=user_story.descripcion,
            horas_estimadas_despues=user_story.horas_estimadas,
            prioridad_despues=user_story.prioridad,
            estado_despues=user_story.estado,
            desarrollador_despues=user_story.desarrollador,
            user_story=user_story,
            accion="Creacion",
            fecha=datetime.date.today(),
            autor=autor
        )

    @staticmethod
    def modificar_registro(user_story, autor):
        registro_user_story = RegistroUserStory.objects.get(user_story=user_story)
        RegistroUserStory.objects.filter(user_story=user_story, autor=autor).update(
            nombre_antes=user_story.nombre,
            descripcion_antes=user_story.descripcion,
            hora_estimada_antes=user_story.hora_estimada,
            prioridad_antes=user_story.prioridad,
            estado_antes=user_story.estado,
            desarrollador_antes=user_story.desarrollador,
            nombre_despues=user_story.nombre,
            descripcion_despues=user_story.descripcion,
            hora_estimada_despues=user_story.hora_estimada,
            prioridad_despues=user_story.prioridad,
            estado_despues=user_story.estado,
            desarrollador_despues=user_story.desarrollador,
            user_story=user_story,
            accion="Modificacion",
            fecha=datetime.date.today(),
            autor=autor
        )

    @staticmethod
    def eliminar_registro(user_story, autor):
        RegistroUserStory.objects.create(
            nombre_antes=user_story.nombre,
            descripcion_antes=user_story.descripcion,
            hora_estimada_antes=user_story.hora_estimada,
            prioridad_antes=user_story.prioridad,
            estado_antes=user_story.estado,
            desarrollador_antes=user_story.desarrollador,
            user_story=user_story,
            accion="Eliminacion",
            fecha=datetime.date.today(),
            autor=autor
        )
