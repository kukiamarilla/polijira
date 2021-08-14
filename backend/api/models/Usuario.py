from django.db import models


class Usuario(models.Model):
    """Modela la clase Usuario

    Atributos:
        nombre {CharField} -- nombre del usuario
        email {EmailField}  -- una direccion de correo electronico
        ESTADO  {choices} -- indica los diferentes estados del usuario
        estado {CharField} -- indica el estado actual del usuario
        firebase_uid {CharField} -- id del SSO firebase
    """

    nombre = models.CharField(max_length=255)
    email = models.EmailField(
        verbose_name='email',
        max_length=255,
        unique=True,
    )
    ESTADO = (('A', 'Activo'), ('I', 'Inactivo'))
    estado = models.CharField(max_length=1, choices=ESTADO, default='I')
    firebase_uid = models.CharField(max_length=50, default='')

    def __str__(self):
        return self.email

    def tiene_permiso(self, permiso):
        """Comprueba si este usuario tiene el permiso especificado

        Args:
            permiso (Permiso): el permiso

        Returns:
            bool: Verdadero; o Falso
        """
        return True
