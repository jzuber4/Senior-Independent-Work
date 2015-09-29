from django.conf import settings
from suds.client import Client as soap_client
import service

if hasattr(settings, 'QUIZ_SERVICE_DEBUG'):
    service.DEBUG = settings.QUIZ_SERVICE_DEBUG

if not service.DEBUG:
    client = soap_client(settings.QUIZ_SERVICE_URL)
    # reload the wsdl for every init
    client.options.cache.clear()
    service.service = client.service
