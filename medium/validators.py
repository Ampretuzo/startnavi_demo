import logging

from django.core.exceptions import ValidationError
from django.conf import settings

from pyhunter import PyHunter


EMAILHUNTER_DELIVERABLE = "deliverable"


logger = logging.getLogger(__name__)

emailhunter_key = getattr(settings, "MEDIUM_EMAILHUNTER_API_KEY", None)
if emailhunter_key:
    hunter = PyHunter(emailhunter_key)


def _emailhunter_verify(email):
    response = hunter.email_verifier(email)
    deliverable = response.get("result", None)
    trust_score = response.get("score", -1)
    if deliverable != EMAILHUNTER_DELIVERABLE:
        logger.info(
            "Someone tried to register with email %s. Emailhunter scores it as : %i - %s",
            email,
            trust_score,
            deliverable,
        )
        raise ValidationError("Email is not trustworthy")


def validate_email_via_emailhunter(value):
    validate_email = getattr(settings, "MEDIUM_EMAILHUNTER_VALIDATION", False)
    if validate_email:
        _emailhunter_verify(value)
    return value
