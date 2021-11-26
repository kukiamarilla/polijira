from django.db import models
from django.contrib.auth.models import User
from backend.api.models import Permiso
from django.core.mail import send_mail
from django.conf import settings


class Usuario(models.Model):
    """Modela la clase Usuario

    Atributos:
        nombre {CharField} -- nombre del usuario
        email {EmailField}  -- una direccion de correo electronico
        ESTADO  {choices} -- indica los diferentes estados del usuario
        estado {CharField} -- indica el estado actual del usuario
        firebase_uid {CharField} -- id del SSO firebase
        rol {ForeignKey} -- rol relacionado a este usuario
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    nombre = models.CharField(max_length=255, default="")
    email = models.EmailField(
        verbose_name='email',
        max_length=255,
        unique=True,
    )
    ESTADO = (('A', 'Activo'), ('I', 'Inactivo'))
    estado = models.CharField(max_length=1, choices=ESTADO, default='I')
    firebase_uid = models.CharField(max_length=50, default='')
    rol = models.ForeignKey('Rol', on_delete=models.CASCADE, null=True, related_name='usuarios')

    def tiene_permiso(self, permiso_codigo):
        """Comprueba si este usuario tiene el permiso especificado

        Args:
            permiso_codigo (String): el codigo del permiso

        Returns:
            bool: True, False
        """
        try:
            self.rol.permisos.get(codigo=permiso_codigo)
            return True
        except Permiso.Permiso.DoesNotExist:
            return False

    def activar(self):
        """
        activar Activa este usuario
        """
        self.estado = "A"
        self.save()

    def desactivar(self):
        """
        desactivar Desactiva este usuario
        """
        self.estado = "I"
        self.save()

    def asignar_rol(self, rol):
        """
        asignar_rol Asigna un rol a este usuario
        """
        self.rol = rol
        self.save()

    def notify(self, notification):
        subject = notification.subject
        message = notification.build_message()
        send_mail(subject, message, settings.EMAIL_HOST_USER, [self.email], html_message=message)
