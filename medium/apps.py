from django.apps import AppConfig
from django.conf import settings


class MediumConfig(AppConfig):
    name = "medium"

    def ready(self):
        clearbit_api_key = getattr(settings, "MEDIUM_CLEARBIT_API_KEY", None)
        clearbit_enrichment = getattr(settings, "MEDIUM_CLEARBIT_ENRICHMENT", False)
        if clearbit_enrichment and clearbit_api_key:
            import clearbit

            clearbit.key = clearbit_api_key
        import medium.signals
