from django.conf import settings
from service import Client
from suds.client import Client as soap_client

client = soap_client(settings.QUIZ_SERVICE_URL)
# reload the wsdl for every init
client.options.cache.clear()
Client.s = client.service
if hasattr(settings, 'QUIZ_SERVICE_DEBUG'):
    Client.debug = settings.QUIZ_SERVICE_DEBUG

