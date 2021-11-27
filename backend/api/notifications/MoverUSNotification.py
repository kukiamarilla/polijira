from django.conf import settings
from backend.api.notifications import Notification


class MoverUSNotification(Notification):

    template = "emails/mover_us.html"
    subject = "[Polijira] Se movió tablero del Kanban"

    def __init__(self, user_story):
        data = {
            "user_story": user_story,
            "url": settings.BASE_URL
        }
        super().__init__(data)
