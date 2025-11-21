import os
import requests
from django.conf import settings
from .adapters import LoggingHTTPAdapter


LOG_ENABLED = getattr(settings, "HTTP_LOG_ENABLED",)

session = requests.Session()
adapter = LoggingHTTPAdapter(
    log_enabled=LOG_ENABLED,
    log_request_body=os.getenv("HTTP_LOG_REQUEST_BODY", "true").lower() == "true",
    log_response_body=os.getenv("HTTP_LOG_RESPONSE_BODY", "true").lower() == "true",
    log_headers=os.getenv("HTTP_LOG_HEADERS", "false").lower() == "true",
    log_url=os.getenv("HTTP_LOG_URL", "true").lower() == "true",
    log_method=os.getenv("LOG_METHOD", "true").lower() == "true",
)

session.mount("http://", adapter)
session.mount("https://", adapter)

def http_request(method, url, **kwargs):
    if not LOG_ENABLED:
        return requests.request(method, url, **kwargs)
    return session.request(method, url, **kwargs)
