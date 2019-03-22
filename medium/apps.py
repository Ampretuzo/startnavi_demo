from django.apps import AppConfig


class MediumConfig(AppConfig):
    name = "medium"

    def ready(self):
        import medium.signals
