import logging
import requests
from django.conf import settings

logger = logging.getLogger(__name__)


def verify_recaptcha(token: str, action: str = "contact_form") -> bool:
    if getattr(settings, "RECAPTCHA_BYPASS", settings.DEBUG):
        return True  # Só ignora se RECAPTCHA_BYPASS estiver ativado

    url = "https://www.google.com/recaptcha/api/siteverify"
    data = {
        "secret": settings.RECAPTCHA_SECRET_KEY,
        "response": token,
    }

    try:
        response = requests.post(url, data=data, timeout=5)
        result = response.json()
    except requests.RequestException as e:
        logger.warning(f"[reCAPTCHA] Erro de conexão: {e}")
        return False

    success = result.get("success", False)
    score = result.get("score", 0)
    received_action = result.get("action", None)

    if not success:
        logger.warning(f"[reCAPTCHA] Verificação falhou: {result}")
        return False

    if received_action != action:
        logger.warning(
            f"[reCAPTCHA] Ação esperada '{action}' mas recebeu '{received_action}'"
        )
        return False

    min_score = getattr(settings, "RECAPTCHA_MIN_SCORE", 0.5)
    if score < min_score:
        logger.warning(f"[reCAPTCHA] Score baixo: {score} (mínimo: {min_score})")
        return False

    return True
