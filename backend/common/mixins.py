import json
import hashlib
from django.conf import settings
from django_redis import get_redis_connection
from rest_framework.response import Response
from rest_framework import status


class IdempotencyMixin:
    """
    Mixin para tornar o método create (POST padrão do DRF) idempotente via Redis.

    Importante:
    - Aplica-se APENAS ao método create().
    - Não cobre @action(methods=["post"]).
    - Actions que exigem idempotência devem implementar lógica própria
      ou delegar explicitamente para este mixin.
    """

    ttl = settings.IDEMPOTENCY_TTL # segundos

    def create(self, request, *args, **kwargs):
        key = request.headers.get("Idempotency-Key")
        if not key:
            return Response(
                {"detail": "Missing Idempotency-Key"},
                status=status.HTTP_400_BAD_REQUEST
            )

        redis = get_redis_connection("default")

        # Hash do corpo para evitar colisões
        body = json.dumps(request.data, sort_keys=True, separators=(",", ":")).encode()
        body_hash = hashlib.sha256(body).hexdigest()
        # A chave inclui hash do payload:
        # mesma Idempotency-Key + payload diferente = nova operação
        redis_key = f"idempotency:{key}:{body_hash}"

        # Tenta obter resposta já registrada
        cached = redis.get(redis_key)
        if cached and cached != b"processing":
            saved = json.loads(cached)
            return Response(
                saved["data"],
                status=saved["status"],
                headers=saved.get("headers", {})
            )

        # SETNX (NX) + TTL (EX)
        inserted = redis.set(redis_key, "processing", nx=True, ex=self.ttl)
        if not inserted:
            # 409 indica concorrência real (race condition),
            # não replay de requisição concluída
            return Response(
                {"detail": "Request already in progress"},
                status=status.HTTP_409_CONFLICT,
            )
        try:
            # processa normalmente
            response = super().create(request, *args, **kwargs)

        except Exception as exc:
            redis.delete(redis_key)
            raise exc

        # Salva resposta consolidada
        payload = {
            "status": response.status_code,
            "data": response.data,
            "headers": {}, # evita headers sensíveis
        }
        redis.set(redis_key, json.dumps(payload), ex=self.ttl)

        return response
