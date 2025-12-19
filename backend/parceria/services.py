"""
Funções de regra de negócio da app parceria.

Objetivo: concentrar lógica de domínio fora de views/serializers/admin,
facilitando manutenção, testes e evolução das regras.
"""

from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import PermissionDenied
from rest_framework.exceptions import ValidationError

from .models import (
    Parceria,
    PedidoServico,
    PedidoItem,
    ContratoServico,
    Servico,
    TicketSuporte,
    TicketMensagem,
)

# ============================================================
# Parceria
# ============================================================

# ============================================================
# Servicos
# ============================================================

# ============================================================
# Contratos
# ============================================================

# ============================================================
# Tickets
# ============================================================


def criar_ticket(parceria: Parceria, tipo_ticket: str, titulo: str, descricao: str):
    """
    Cria um ticket de suporte.

    mensagem: {"autor": User, "conteudo": conteudo}.

    Regras:
    - parceria obrigatoria
    - descrição obrigatoria e limitada a 4000 caracteres.
    - titulo limitado a 60 caracteres.
    - tipo padrão se não informado
    - atomicidade
    """
    DESC_CHAR_LIMIT = 4000
    TITULO_CHAR_LIMIT = 60

    if not parceria:
        raise PermissionDenied("Usuário não está vinculado a uma parceria.")

    if not descricao or len(descricao.strip()) == 0:
        raise ValidationError("Descrição do ticket é obrigatoria.")

    if len(descricao) > DESC_CHAR_LIMIT:
        raise ValidationError(
            f"Descrição excede o limite de {DESC_CHAR_LIMIT} caracteres."
        )

    if len(titulo) > TITULO_CHAR_LIMIT:
        raise ValidationError(
            f"Titulo excede o limite de {TITULO_CHAR_LIMIT} caracteres."
        )

    if not tipo_ticket:
        tipo_ticket = TicketSuporte.TicketSuporteTipo.OUTRO

    with transaction.atomic():
        ticket = TicketSuporte.objects.create(
            parceria=parceria,
            tipo_ticket_suporte=tipo_ticket,
            titulo=titulo,
            descricao=descricao,
            status_ticket_suporte=TicketSuporte.TicketSuporteStatus.NOVO,
            data_criacao=timezone.now(),
        )
        return ticket


def responder_ticket(ticket: TicketSuporte, usuario, conteudo: str) -> TicketMensagem:
    """
    Registra uma resposta em um ticket de suporte.
    Regras:
    - Apenas tickets não fechados podem receber respostas.
    - Se o ticket estiver em estado NOVO, muda automaticamente para EM_ANALISE.
    """

    CONT_CHAR_LIMIT = 4000

    if not usuario or not usuario.is_authenticated:
        raise ValidationError("Usuário não autenticado.")

    if ticket.status_ticket_suporte == TicketSuporte.TicketSuporteStatus.CONCLUIDO:
        raise ValidationError(
            "Não é permitido responder um ticket marcado como concluido."
        )

    if ticket.status_ticket_suporte == TicketSuporte.TicketSuporteStatus.REJEITADO:
        raise ValidationError(
            "Não é permitido responder um ticket marcado como rejeitado."
        )

    if len(conteudo) > CONT_CHAR_LIMIT:
        raise ValidationError(
            f"A mensagem excede o limite de {CONT_CHAR_LIMIT} caracteres."
        )

    if ticket.status_ticket_suporte == TicketSuporte.TicketSuporteStatus.NOVO:
        ticket.status_ticket_suporte = TicketSuporte.TicketSuporteStatus.EM_ANALISE
        ticket.save(update_fields=["status_ticket_suporte"])

    mensagem = TicketMensagem.objects.create(
        ticket=ticket,
        autor=usuario,
        conteudo=conteudo,
    )

    return mensagem


# ============================================================
# Pedidos
# ============================================================


def criar_pedido(
    parceria: Parceria, itens: list[dict], status_pedido_servico: str = None
):
    """
    Cria um pedido com múltiplos itens de serviço.

    itens: {"servico": Servico, "recorrente": bool, "data_renovacao": datetime}

    Regras:
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
        pedido.refresh_from_db()  # evita concluir objeto desatualizado

        # Regra 1:somente pedidos em andamento podem ser concluídos
        if (
            pedido.status_pedido_servico
            != PedidoServico.PedidoServicoStatus.EM_ANDAMENTO
        ):
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
                raise ValidationError(f"Serviço '{item.servico.nome}' está inativo.")

        pedido.status_pedido_servico = PedidoServico.PedidoServicoStatus.CONCLUIDO
        pedido.data_fim = timezone.now()

        pedido.save(update_fields=["status_pedido_servico", "data_fim"])

        return pedido


def cancelar_pedido(pedido: PedidoServico) -> PedidoServico:
    """
    Marca um pedido como cancelado

    1. Somente EM_ANDAMENTO ou PENDENTE podem ser cancelados.
    2. Registra data_fim e cancelado_por (se houver campo).
    """
    status_cancelaveis = (
        PedidoServico.PedidoServicoStatus.EM_ANDAMENTO,
        PedidoServico.PedidoServicoStatus.PENDENTE,
    )

    with transaction.atomic():
        pedido.refresh_from_db()  # evita cancelar objeto desatualizado

        if pedido.status_pedido_servico not in status_cancelaveis:
            raise ValidationError(
                f"pedido no status '{pedido.status_pedido_servico}' não pode ser cancelado. status permitidos: 'PENDENTE e EM_ANDAMENTO'"
            )

        pedido.status_pedido_servico = PedidoServico.PedidoServicoStatus.CANCELADO
        pedido.data_fim = timezone.now()

        pedido.save(update_fields=["status_pedido_servico", "data_fim"])

        return pedido
