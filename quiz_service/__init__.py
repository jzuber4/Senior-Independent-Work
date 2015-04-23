from django.conf import settings
from service import Client
from suds.client import Client as soap_client

Client.s = soap_client(settings.QUIZ_SERVICE_URL).service
