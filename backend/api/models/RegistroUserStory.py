from django.db import models
import datetime

ESTADOS_US = (
    ("P", "Pendiente"),
    ("R", "Release"),
    ("C", "Cancelado"),
    ("E", "Eliminado")
)

ESTADOS_ESTIMADOS = (
    ("N", "No estimado"),
    ("P", "Parcial"),
    ("C", "Completo")
)


class RegistroUserStory(models.Model):
    """
    RegistroUserStory Modela el Registro de User Stories.
    Guarda todos los user stories creados, modificados o eliminados

    Args:
        models (Model): Modelo de django

    Atributes:
        nombre_antes (CharField): Nombre del User Story al modificar o eliminar
        descripcion_antes (TextField): Descripcion del User Story al modificar o eliminar
        hora_estimada_antes (IntegerField): Hora estimada del User Story al modificar o eliminar
        prioridad_antes (IntegerField): Prioridad del User Story al modificar o eliminar
        estado_antes (CharField): Estado del User Story al modificar o eliminar
        desarrollador_antes (ForeignKey): Desarrollador del User Story al modificar o eliminar
        nombre_despues (CharField): Nombre del User Story al crear o modificar
        descripcion_despues (TextField): Descripcion del User Story al crear o modificar
        hora_estimada_despues (IntegerField): Hora estimada del User Story al crear o modificar
        prioridad_despues (IntegerField): Prioridad del User Story al crear o modificar
        estado_despues (CharField): Estado del User Story al crear o modificar
        desarrollador_despues (ForeignKey): Desarrollador del User Story al crear o modificar
        user_story (OneToOneField): User Story que se registra
        accion (CharField): Indica si se realizo una creación, modificación o eliminación
        autor (ForeignKey): Miembro que realiza el registro
    """
    nombre_antes = models.CharField(max_length=255, null=True)
    descripcion_antes = models.TextField(null=True)
    horas_estimadas_antes = models.IntegerField(null=True)
    prioridad_antes = models.IntegerField(null=True)
    estado_antes = models.CharField(max_length=1, choices=ESTADOS_US, null=True)
    desarrollador_antes = models.ForeignKey("Miembro", on_delete=models.CASCADE,
                                            related_name="registros_antes", null=True)
    nombre_despues = models.CharField(max_length=255, null=True)
    descripcion_despues = models.TextField(null=True)
    horas_estimadas_despues = models.IntegerField(null=True)
    prioridad_despues = models.IntegerField(null=True)
    estado_despues = models.CharField(max_length=1, choices=ESTADOS_US, null=True)
    desarrollador_despues = models.ForeignKey(
        "Miembro", on_delete=models.CASCADE, related_name="registros_despues", null=True)
    user_story = models.ForeignKey("UserStory", on_delete=models.CASCADE, related_name="registros")
    accion = models.CharField(max_length=50)
    fecha = models.DateField()
    autor = models.ForeignKey("Miembro", on_delete=models.CASCADE, related_name="registros")

    @staticmethod
    def crear_registro(user_story, autor):
        RegistroUserStory.objects.create(
            nombre_despues=user_story.nombre,
            descripcion_despues=user_story.descripcion,
            prioridad_despues=user_story.prioridad,
            estado_despues=user_story.estado,
            user_story=user_story,
            accion="Creacion",
            fecha=datetime.date.today(),
            autor=autor
        )

    @staticmethod
    def modificar_registro(user_story, autor):
        registro = RegistroUserStory.objects.filter(user_story=user_story).order_by("-id")[0]
        RegistroUserStory.objects.create(
            nombre_antes=registro.nombre_despues,
            descripcion_antes=registro.descripcion_despues,
            horas_estimadas_antes=registro.horas_estimadas_despues,
            prioridad_antes=registro.prioridad_despues,
            estado_antes=registro.estado_despues,
            desarrollador_antes=registro.desarrollador_despues,
            nombre_despues=user_story.nombre,
            descripcion_despues=user_story.descripcion,
            horas_estimadas_despues=user_story.horas_estimadas,
            prioridad_despues=user_story.prioridad,
            estado_despues=user_story.estado,
            desarrollador_despues=user_story.desarrollador.miembro_proyecto if user_story.desarrollador is not None else None,
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
            horas_estimadas_antes=user_story.horas_estimadas,
            prioridad_antes=user_story.prioridad,
            estado_antes=user_story.estado,
            desarrollador_antes=user_story.desarrollador.miembro_proyecto if user_story.desarrollador is not None else None,
            user_story=user_story,
            accion="Eliminacion",
            fecha=datetime.date.today(),
            autor=autor
        )
