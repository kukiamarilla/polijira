from backend.api.models import Message


def create_message():
    Message.objects.create(
        subject="Test Message",
        body="This is a test message"
    )
