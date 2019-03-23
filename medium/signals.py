from django.conf import settings
from django.dispatch import receiver

from djoser import signals as djoser_signals
from djoser import views as djoser_views
import clearbit

from . import models


def _populate_enrichment_data(enrichment_data, clearbit_response):
    if "person" in clearbit_response:
        person_data = clearbit_response["person"]
        if "name" in person_data:
            enrichment_data.first_name = person_data["name"].get("givenName", "") or ""
            enrichment_data.last_name = person_data["name"].get("familyName", "") or ""
        if "geo" in person_data:
            enrichment_data.country = person_data["geo"].get("country", "") or ""
    if "company" in clearbit_response:
        company_data = clearbit_response["company"]
        enrichment_data.company_clearbit_id = company_data.get("id", "") or ""
        enrichment_data.company_name = company_data.get("name", "") or ""
        enrichment_data.company_legal_name = company_data.get("legalName", "") or ""
        enrichment_data.company_domain = company_data.get("domain", "") or ""
        if "metrics" in company_data:
            enrichment_data.company_employees_range = (
                company_data["metrics"].get("employeesRange", "") or ""
            )


@receiver(djoser_signals.user_registered, sender=djoser_views.UserCreateView)
def user_registered(user, request, **kwargs):
    models.UserProfile.objects.create(user=user)
    """TODO: Celery Celery Celery Celery Celery Celery Celery Celery Celery
    Right now, I'm using blocking api for simplicity"""
    enrichment_data = models.UserEnrichmentData(user=user)
    clearbit_enrichment = getattr(settings, "MEDIUM_CLEARBIT_ENRICHMENT", False)
    if not clearbit_enrichment:
        enrichment_data.enrichment_run = False
    else:
        email = user.email
        response = clearbit.Enrichment.find(email=email, stream=True)
        if response:
            _populate_enrichment_data(enrichment_data, response)
        enrichment_data.enrichment_run = True
    enrichment_data.save()
