from django.conf import settings
from backend.api.notifications import Notification


class USDoneNotification(Notification):

    template = "emails/us_done.html"
    subject = "[Polijira] El User Story está listo para control de calidad"

    def __init__(self, user_story):
        data = {
            "user_story": user_story,
            "url": settings.BASE_URL
        }
        super().__init__(data)
