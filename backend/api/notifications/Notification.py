from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


class Notification:
    """
    Notification Modela las notificaciones que reciben los usuarios

    Atributes:
        template (str): template a enviar
        subject (str): subject a enviar
    """
    template = ""
    subject = ""

    def __init__(self, data):
        self.data = data

    def build_message(self):
        """
        build_message Convierte a String el dato a enviar

        Returns:
            str: dato a str
        """
        return render_to_string(self.template, self.data)

    def notify_all(self, usuarios):
        """
        notify_all Notifica a varios usuarios

        Args:
            usuarios (list Usuario): Lista de Usuarios
        """
        emails = list(map(lambda usuario: usuario.email, usuarios))
        message = self.build_message()
        send_mail(self.subject, message, settings.EMAIL_HOST_USER, emails, html_message=message)
