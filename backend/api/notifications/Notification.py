from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


class Notification:
    template = ""
    subject = ""

    def __init__(self, data):
        self.data = data

    def build_message(self):
        return render_to_string(self.template, self.data)

    def notify_all(self, usuarios):
        emails = list(map(lambda usuario: usuario.email, usuarios))
        message = self.build_message()
        send_mail(self.subject, message, settings.EMAIL_HOST_USER, emails, html_message=message)
