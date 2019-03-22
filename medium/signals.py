from django.dispatch import receiver

from djoser import signals as djoser_signals
from djoser import views as djoser_views
import clearbit

from . import models


@receiver(djoser_signals.user_registered, sender=djoser_views.UserCreateView)
def user_registered(user, request, **kwargs):
    models.UserProfile.objects.create(user=user)
    """TODO: implement enrichment using Celery
    Right now, I'm using blocking api for simplicity"""
    # email = user.email
    # response = clearbit.Enrichment.find(email=email, stream=True)
    enrichment_data = models.UserEnrichmentData(user=user)
    enrichment_data.save()
