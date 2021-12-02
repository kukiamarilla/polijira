from .Notification import Notification

from django.conf import settings


class RespuestaEstimacionNotification(Notification):

    template = "emails/respuesta_estimacion.html"
    subject = "[PoliJira] Estimación de User Story Respondida."

    def __init__(self, sprintbacklog):
        data = {
            "sprintbacklog": sprintbacklog,
            "proyecto": sprintbacklog.user_story.proyecto,
            "url": settings.BASE_URL
        }
        super().__init__(data)
