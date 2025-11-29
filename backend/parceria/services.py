"""
Funções de regra de negócio da app parceria.

Objetivo: concentrar lógica de domínio fora de views/serializers/admin,
facilitando manutenção, testes e evolução das regras.
"""

from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import PermissionDenied
from django.core.exceptions import ValidationError

from .models import (
    Parceria,
    PedidoServico,
    PedidoItem,
    ContratoServico,
    Servico,
    TicketSuporte,
)


# ============================================================
# Pedidos
# ============================================================

def criar_pedido(parceria: Parceria, itens: list[dict], status_pedido_servico: str = None):
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

def concluir_pedido(pedido: PedidoServico) -> PedidoServico:
    """
    Marca pedido como concluído.

    Regras:
    1. somente pedidos em andamento podem ser concluídos
    2. pedidos sem itens não pode ser concluído.
    3. pedidos recorrentes sem data de renovação não podem ser concluídos.
    4. Pedidos com Serviços inativos não podem ser concluídos.
    """

    with transaction.atomic():
        pedido.refresh_from_db() # evita concluir objeto desatualizado

        # Regra 1:somente pedidos em andamento podem ser concluídos
        if pedido.status_pedido_servico != PedidoServico.PedidoServicoStatus.EM_ANDAMENTO:
            raise ValidationError("Somente pedidos em andamento podem ser concluídos.")

        # Regra 2:pedidos sem itens não pode ser concluído.
        itens = list(pedido.itens.select_related("servico"))
        if not itens:
            raise ValidationError("Pedido sem itens não pode ser concluído.")

        for item in itens:
            # Regra 3:pedidos recorrentes sem data de renovação não podem ser concluídos.
            if item.recorrente and not item.data_renovacao:
                raise ValidationError(
                    f"Item {item.id} recorrente sem data de renovação."
                )

            # Regra 4: Pedidos com Serviços inativos não podem ser concluídos.
            if not item.servico.ativo:
                raise ValidationError(
                    f"Serviço '{item.servico.nome}' está inativo."
                )

        pedido.status_pedido_servico = PedidoServico.PedidoServicoStatus.CONCLUIDO
        pedido.data_fim = timezone.now()

        pedido.save(update_fields=["status_pedido_servico", "data_fim"])

        return pedido
