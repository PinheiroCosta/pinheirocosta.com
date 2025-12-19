import logging
import time
import requests
from requests.adapters import HTTPAdapter

logger = logging.getLogger("backend.http")

SENSITIVE_HEADERS = {"authorization", "cookie", "set-cookie"}


class LoggingHTTPAdapter(HTTPAdapter):
    """
    Adapter that logs outgoing HTTP requests/responses.
    Controlled by settings.HTTP_LOG_ENABLED.

    Do not enable in production unless debugging microservice issues.
    """

    def __init__(
        self,
        log_request_body=True,
        log_response_body=True,
        log_headers=False,
        log_url=True,
        log_method=True,
        log_enabled=False,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.log_request_body = log_request_body
        self.log_response_body = log_response_body
        self.log_headers = log_headers
        self.log_url = log_url
        self.log_method = log_method
        self.log_enabled = log_enabled

    def _safe_headers(self, headers):
        if not self.log_headers:
            return None
        clean = {}
        for k, v in headers.items():
            if k.lower() in SENSITIVE_HEADERS:
                clean[k] = "***REDACTED***"
            else:
                clean[k] = v
        return clean

    def _safe_body(self, body):
        if not self.log_request_body or not body:
            return None
        if isinstance(body, bytes):
            body = body.decode("utf-8", errors="ignore")
        try:
            return json.loads(body)
        except Exception:
            return body

    def send(self, request, **kwargs):
        if not self.log_enabled:
            return super().send(request, **kwargs)

        start = time.time()

        request_method = request.method if self.log_method else None
        request_url = request.url if self.log_url else None
        request_headers = request.headers if self.log_headers else None

        request_body = None
        if self.log_request_body and request.body:
            try:
                request_body = json.loads(request.body)
            except Exception:
                request_body = request.body

        msg = "REQUEST ->"
        if request_method:
            msg += f" {request_method}"
        if request_url:
            msg += f" {request_url}"
        if request_headers:
            msg += f" | headers={self._safe_headers(request_headers)}"
        if request_body:
            msg += f" | body={self._safe_body(request_body)}"

        logger.debug(msg)

        response = super().send(request, **kwargs)
        elapsed = round(time.time() - start, 3)

        response_body = None
        if self.log_response_body:
            try:
                response_body = response.json()
            except Exception:
                response_body = response.text

        msg = f"RESPONSE <- status={response.status_code} | time={elapsed}s"
        if response_body:
            msg += f" | body={response_body}"

        logger.debug(msg)

        return response
