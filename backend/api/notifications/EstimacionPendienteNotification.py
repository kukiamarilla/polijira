from .Notification import Notification

from django.conf import settings


class EstimacionPendienteNotification(Notification):

    template = "emails/estimacion_pendiente.html"
    subject = "[PoliJira] Estimación pendiente."

    def __init__(self, user_story):
        data = {
            "user_story": user_story,
            "url": settings.BASE_URL
        }
        super().__init__(data)
