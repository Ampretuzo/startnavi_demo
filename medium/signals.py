from django.dispatch import receiver

from djoser import signals as djoser_signals
from djoser import views as djoser_views
import clearbit

from . import models
from .app_settings import MEDIUM_CLEARBIT_ENRICHMENT


def _populate_enrichment_data(enrichment_data, clearbit_response):
    if "person" in clearbit_response:
        person_data = clearbit_response["person"]
        if "name" in person_data:
            enrichment_data.first_name = person_data["name"].get("givenName", "")
            enrichment_data.last_name = person_data["name"].get("familyName", "")
        if "geo" in person_data:
            enrichment_data.country = person_data["geo"].get("country", "")
    if "company" in clearbit_response:
        company_data = clearbit_response["company"]
        enrichment_data.company_clearbit_id = company_data.get("id", "")
        enrichment_data.company_name = company_data.get("name", "")
        enrichment_data.company_legal_name = company_data("legalName", "")
        enrichment_data.company_domain = company_data.get("domain", "")
        if "metrics" in company_data:
            enrichment_data.company_employees_range = company_data["metrics"].get(
                "employeesRange", ""
            )


@receiver(djoser_signals.user_registered, sender=djoser_views.UserCreateView)
def user_registered(user, request, **kwargs):
    models.UserProfile.objects.create(user=user)
    """TODO: Celery Celery Celery Celery Celery Celery Celery Celery Celery
    Right now, I'm using blocking api for simplicity"""
    enrichment_data = models.UserEnrichmentData(user=user)
    if not MEDIUM_CLEARBIT_ENRICHMENT:
        enrichment_data.enrichment_run = False
    else:
        email = user.email
        response = clearbit.Enrichment.find(email=email, stream=True)
        if response:
            _populate_enrichment_data(enrichment_data, response)
        enrichment_data.enrichment_run = True
    enrichment_data.save()
