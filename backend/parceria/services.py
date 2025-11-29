"""
Funções de regra de negócio da app parceria.

Objetivo: concentrar lógica de domínio fora de views/serializers/admin,
facilitando manutenção, testes e evolução das regras.
"""

from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import PermissionDenied

from .models import (
    PedidoServico,
    PedidoItem,
    ContratoServico,
    Servico,
    TicketSuporte,
)


# ============================================================
# Pedidos
# ============================================================

def criar_pedido(parceria, itens, status_pedido_servico=None):
    """
    Cria um pedido com múltiplos itens de serviço.

    itens: lista de dicts {"servico": Servico, "recorrente": bool, "data_renovacao": datetime}

    Regras aplicadas:
    - atomicidade
    - validação de serviços
    - criação consistente de itens
    """
    if not status_pedido_servico:
        status_pedido_servico = PedidoServico.PedidoServicoStatus.PENDENTE

    if not parceria:
        raise PermissionDenied("Usuário não está vinculado a uma parceria.")

    with transaction.atomic():
        pedido = PedidoServico.objects.create(
            parceria=parceria,
            status_pedido_servico=status_pedido_servico,
            data_inicio=timezone.now(),
        )

        for item in itens:
            servico = item["servico"]

            PedidoItem.objects.create(
                pedido=pedido,
                servico=servico,
                recorrente=item.get("recorrente", False),
                data_renovacao=item.get("data_renovacao"),
            )

        return pedido

