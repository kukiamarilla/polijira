from django.template.loader import render_to_string


class Notification:
    template = ""
    subject = ""

    def __init__(self, data):
        self.data = data

    def build_message(self):
        return render_to_string(self.template, self.data)
