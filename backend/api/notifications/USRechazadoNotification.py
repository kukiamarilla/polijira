from django.conf import settings
from backend.api.notifications import Notification


class USRechazadoNotification(Notification):
    """
    USRechazadoNotification Clase para representar una Notificacion al rechazar un User Story

    Args:
        Notification (class): Hereda de Notification
    """
    template = "emails/us_rechazado.html"
    subject = "[Polijira] El QA rechazó su User Story"

    def __init__(self, user_story):
        data = {
            "user_story": user_story,
            "url": settings.BASE_URL
        }
        super().__init__(data)
