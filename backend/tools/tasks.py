from celery import shared_task
from django.core.cache import cache
from common.models import ParametroSistema
import requests

@shared_task
def ping_stringutils_healthcheck():
    try:
        param = ParametroSistema.objects.get(chave="STRINGUTILS_KEEPALIVE_URL")
        url = param.valor
    except ParametroSistema.DoesNotExist:
        return "Ping failed: ParametroSistema 'STRINGUTILS_KEEPALIVE_URL' not found"

    cache_key = "stringutils_last_successful_ping"
    last_success = cache.get(cache_key)
    timeout = 5 if last_success else 60

    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        cache.set(cache_key, True, timeout=3600)
        return f"Ping OK: {response.status_code} (timeout={timeout}s)"
    except Exception as e:
        cache.delete(cache_key)
        return f"Ping failed (timeout={timeout}s): {e}"
