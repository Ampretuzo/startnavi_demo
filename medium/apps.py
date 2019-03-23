from django.apps import AppConfig

from .app_settings import MEDIUM_CLEARBIT_ENRICHMENT, MEDIUM_CLEARBIT_API_KEY


class MediumConfig(AppConfig):
    name = "medium"

    def ready(self):
        if MEDIUM_CLEARBIT_ENRICHMENT:
            import clearbit

            clearbit.key = MEDIUM_CLEARBIT_API_KEY
        import medium.signals
