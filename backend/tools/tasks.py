import requests
from celery import shared_task

@shared_task
def ping_stringutils_healthcheck():
    url = "https://stringutils-601a.onrender.com/api/v1/stringutils/health"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return f"Ping OK: {response.status_code}"
    except Exception as e:
        return f"Ping failed: {e}"
