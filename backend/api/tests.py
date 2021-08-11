from django.test import TestCase
from .models import Message
# Create your tests here.


class ExampleTest(TestCase):

    def setUp(self):
        self.message = Message.objects.create(
            subject="Example Message",
            body="This is an example."
        )

    def test_message_model(self):
        print("\nTesting Message model.")
        m = self.message
        self.assertTrue(isinstance(m, Message))
        self.assertEquals(str(m), "Example Message: This is an example.")
