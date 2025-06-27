import re
import bleach
from rest_framework import serializers


TAG_RE = re.compile(r"<[^>]+>")


def contains_html(text: str) -> bool:
    return bool(TAG_RE.search(text))


def sanitize_html(text: str) -> str:
    """
    Remove qualquer tag HTML da string.
    """
    return bleach.clean(text, tags=[], strip=True)


def validate_no_html(field_name: str, value: str) -> str:
    """
    Valida que o campo não contenha HTML.
    """
    if contains_html(value):
        raise serializers.ValidationError(
            f"HTML não é permitido no campo '{field_name}'."
        )
    return value


def sanitize_text(value: str, tags: list[str] = []) -> str:
    """
    Remove qualquer tag HTML ou JS do valor.
    Pode permitir tags específicas se desejado.
    """
    return bleach.clean(value, tags=tags, strip=True)


def contains_sql_keywords(text: str) -> bool:
    """
    Retorna verdadeiro se o campo conter SQL
    """
    sql_payloads = [
        "DROP TABLE",
        "DELETE FROM",
        "INSERT INTO",
        "UPDATE",
        "SELECT * FROM",
        "' OR '1'='1",
        "--",
        ";--",
        "'--",
        "'#",
        "' or 1=1",
        "xp_cmdshell",
    ]
    lowered = text.lower()
    return any(payload.lower() in lowered for payload in sql_payloads)


def validate_no_sql_injection(field_name: str, value: str) -> str:
    """
    Valida que o campo não contenha SQL.
    """
    if contains_sql_keywords(value):
        raise serializers.ValidationError(
            f"Entrada suspeita de SQL injection no campo '{field_name}'."
        )
    return value
