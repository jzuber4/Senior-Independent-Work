from django.conf import settings
from suds.client import Client as soap_client
import service

if hasattr(settings, 'QUIZ_SERVICE_DEBUG'):
    service.DEBUG = settings.QUIZ_SERVICE_DEBUG

try:
    client = soap_client(settings.QUIZ_SERVICE_URL)
    # reload the wsdl for every init
    client.options.cache.clear()
    service.service = client.service
except Exception as e:
    if service.DEBUG:
        print("ERROR ON QUIZ SERVICE INIT: {}".format(e))
    else:
        raise
