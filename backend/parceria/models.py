from django.conf import settings
from django.db import models
from django.utils import timezone


class BaseAtivoHistorico(models.Model):
    """
    Modelo abstrato para entidades com ciclo de vida (ativo, início, fim).
    """

    ativo = models.BooleanField(
        default=True, help_text="Indica se o registro está ativo no momento."
    )
    data_inicio = models.DateTimeField(
        default=timezone.now, help_text="Data/hora em que o registro entrou em vigor."
    )
    data_fim = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Data/hora de encerramento do registro, se houver.",
    )

    class Meta:
        abstract = True


class Servico(BaseAtivoHistorico):
    """
    Representa um serviço disponível no catálogo da plataforma.
    É a lista de opções que podem ser oferecidas aos clientes.
    Aqui ficam informações estáticas como nome, descrição, e preço base.
    """

    nome = models.CharField(
        max_length=100, help_text="Nome do serviço oferecido no catálogo."
    )
    descricao = models.TextField(
        blank=True, help_text="Descrição do serviço exibida para o cliente."
    )
    preco_base = models.DecimalField(
        max_digits=8, decimal_places=2, help_text="Preço base do serviço."
    )

    def __str__(self):
        return self.nome


class Parceria(BaseAtivoHistorico):
    """
    Representa uma relação de parceria com uma pessoa física ou jurídica.

    Regras de auditoria e encerramento:
    - Caso a parceria precise ser retomada no futuro, um **novo registro** deve ser criado,
      preservando o histórico para auditoria.
    """

    class NaturezaParceria(models.TextChoices):
        PF = "pf", "Pessoa Física"
        PJ = "pj", "Pessoa Jurídica"

    class CategoriaParceria(models.TextChoices):
        CLIENTE = (
            "cliente",
            "Cliente",
        )  # parceiro que contrata os serviços/produtos do site.
        MARCA = (
            "marca",
            "Marca",
        )  # empresas para co-marketing, licenciamento, divulgação.
        CONTEUDO = (
            "conteudo",
            "Criador de conteúdo",
        )  # criadores de conteúdo, influenciadores, afiliados.
        TECNOLOGIA = (
            "tecnologia",
            "Tecnologia",
        )  # integrações de API, provedores SaaS, hospedagem.
        FORNECEDOR = (
            "fornecedor",
            "Fornecedor",
        )  # parceiros que entregam insumos/serviços para nós
        DISTRIBUIDOR = (
            "distribuidor",
            "Distribuidor",
        )  # parceiros que levam o serviço a terceiros (marketplaces, revendedores).
        SOCIAL = "social", "Social"  # iniciativas de impacto social ou cultural.
        COMUNIDADE = "comunidade", "Comunidade"  # grupos open source, fóruns, eventos.

    nome = models.CharField(
        max_length=100, help_text="Nome da pessoa física ou jurídica parceira."
    )
    natureza = models.CharField(
        max_length=2,
        choices=NaturezaParceria.choices,
        help_text="Indica se a parceria é pessoa física ou pessoa jurídica.",
    )
    categoria = models.CharField(
        max_length=20,
        choices=CategoriaParceria.choices,
        help_text="Classificação da relação comercial.",
    )
    proprietario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="parcerias_proprietario",
        help_text="Usuário principal responsável pela parceria.",
    )
    dominio = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Domímio personalizado do cliente, se houver.",
    )

    def __str__(self):
        return f"{self.nome} ({self.proprietario.get_full_name()})"


class ParceriaMembro(BaseAtivoHistorico):
    """
    Usuários vinculados a uma parceria.
    Todo membro listado aqui é colaborador; o proprietário está definido em Parceria.proprietario.
    """

    parceria = models.ForeignKey(
        Parceria,
        on_delete=models.CASCADE,
        related_name="membros",
        help_text="Parceria a qual o membro pertence.",
    )
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="parcerias_membro",
        help_text="Usuário membro colaborador.",
    )

    class Meta:
        unique_together = ("parceria", "usuario")
        verbose_name = "Membro de Parceria"
        verbose_name_plural = "Membros de Parceria"

    def __str__(self):
        return f"{self.usuario.get_username()} em {self.parceria.nome}"


class ContratoServico(BaseAtivoHistorico):
    """
    Representa o acordo formal entre a parceria (cliente) e a plataforma
    para a entrega de um ou mais serviços. Define início, término, e observações gerais do contrato.
    """

    parceria = models.ForeignKey(
        Parceria,
        on_delete=models.CASCADE,
        related_name="contratos",
        help_text="Parceria a qual o contrato pertence",
    )
    observacoes = models.TextField(
        blank=True, help_text="Notas gerais sobre o contrato, ou termos específicos."
    )

    class Meta:
        verbose_name = "Contrato de Serviço"
        verbose_name_plural = "Contratos de Serviço"

    def __str__(self):
        return f"{self.parceria} - ({self.data_inicio})"


class ServicoContratado(BaseAtivoHistorico):
    """
    Representa um serviço específico vinculado a um contrato de serviço.
    Cada serviço pode ter ciclo próprio de uso e de cobrança.
    """

    contrato_servico = models.ForeignKey(
        ContratoServico,
        on_delete=models.CASCADE,
        related_name="servicos_contratados",
        help_text="Contrato ao qual este serviço contratado está vínculado.",
    )
    servico = models.ForeignKey(
        Servico,
        on_delete=models.CASCADE,
        related_name="servicos_contratados",
        help_text="Serviço adquirido pelo cliente dentro deste contrato.",
    )
    recorrente = models.BooleanField(
        default=False, help_text="Indica se serviço possui renovação periódica."
    )
    pedido_item = models.ForeignKey(
        "PedidoItem",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="servicos_contratados",
        help_text="Item de pedido que originou este serviço, usado para auditoria.",
    )

    def __str__(self):
        origem = (
            f" / origem: PedidoItem {self.pedido_item_id}"
            if self.pedido_item_id
            else ""
        )
        return f"{self.servico.nome} - Contrato {self.contrato_servico.id}{origem}"


class ContratoCobranca(models.Model):
    """
    Representa uma cobrança financeira associada a um serviço contratado.
    É a obrigação de pagamento do cliente para manter o serviço ativo.
    """

    servico_contratado = models.ForeignKey(
        ServicoContratado,
        on_delete=models.CASCADE,
        related_name="cobrancas",
        help_text="Serviço contratado a qual pertence esta cobrança.",
    )
    valor = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="Valor a ser cobrado do cliente."
    )
    vencimento = models.DateField(help_text="Data de vencimento da cobrança.")
    data_pagamento = models.DateField(
        null=True, blank=True, help_text="Data em que a cobrança foi paga, se houver."
    )

    def __str__(self):
        return f"Cobrança {self.valor} - {self.servico_contratado.servico.nome}"


class PedidoServico(BaseAtivoHistorico):
    """
    Intenção inicial do cliente: solicitação de um serviço.
    Pode ou não evoluir para um contrato formal.
    O status acompanha o ciclo do pedido (pendente → andamento → concluído/cancelado).
    """

    class PedidoServicoStatus(models.TextChoices):
        PENDENTE = "pendente", "Pendente"
        EM_ANDAMENTO = "em_andamento", "Em andamento"
        CONCLUIDO = "concluido", "Concluído"
        CANCELADO = "cancelado", "Cancelado"

    parceria = models.ForeignKey(
        Parceria,
        on_delete=models.CASCADE,
        related_name="pedidos",
        help_text="Parceria que abriu o pedido de serviço.",
    )
    status_pedido_servico = models.CharField(
        max_length=20,
        choices=PedidoServicoStatus.choices,
        default=PedidoServicoStatus.PENDENTE,
        help_text="Status atual do pedido dentro do fluxo operacional.",
    )

    class Meta:
        verbose_name_plural = "Pedidos"

    def __str__(self):
        return f"Pedido {self.id} - {self.parceria.nome}"


class PedidoItem(models.Model):
    """
    Item de um pedido de serviço. Permite que um pedido agrupe vários serviços.
    """

    pedido = models.ForeignKey(
        PedidoServico,
        on_delete=models.CASCADE,
        related_name="itens",
        help_text="Pedido ao qual este item pertence.",
    )
    servico = models.ForeignKey(
        Servico, on_delete=models.PROTECT, help_text="Serviço solicitado neste item."
    )
    data_renovacao = models.DateTimeField(
        blank=True, null=True, help_text="Data prevista para renovação, se aplicável."
    )
    recorrente = models.BooleanField(
        default=False, help_text="Indica se o serviço deve ser renovado."
    )


class TicketSuporte(models.Model):
    """
    Registro de solicitações de suporte abertas por clientes.
    Pode ser sugestão, dúvida, problema ou outro.
    Possui ciclo de vida (novo → análise → execução → concluído/rejeitado).
    """

    class TicketSuporteTipo(models.TextChoices):
        SUGESTAO = "sugestao", "Sugestão de funcionalidade"
        AJUDA = "ajuda", "Ajuda ou dúvida"
        PROBLEMA = "problema", "Relato de problema"
        OUTRO = "outro", "Outro"

    class TicketSuporteStatus(models.TextChoices):
        NOVO = "novo", "Novo"
        EM_ANALISE = "em_analise", "Em análise"
        EM_EXECUCAO = "em_execucao", "Em execução"
        CONCLUIDO = "concluido", "Concluído"
        REJEITADO = "rejeitado", "Rejeitado"

    parceria = models.ForeignKey(
        Parceria, on_delete=models.CASCADE, help_text="Parceria que abriu o ticket."
    )
    tipo_ticket_suporte = models.CharField(
        max_length=20,
        choices=TicketSuporteTipo.choices,
        help_text="Tipo de solicitação.",
    )
    titulo = models.CharField(max_length=120, help_text="Título curto da solicitação")
    descricao = models.TextField(help_text="Descrição detalhada da solicitação.")
    status_ticket_suporte = models.CharField(
        max_length=20,
        choices=TicketSuporteStatus.choices,
        default=TicketSuporteStatus.NOVO,
        help_text="Status atual do ticket.",
    )
    data_criacao = models.DateTimeField(
        auto_now_add=True, help_text="Data/hora em que o ticket foi criado."
    )
    prazo_entrega = models.DateTimeField(
        blank=True, null=True, help_text="Prazo estimado para resolução, se definido."
    )

    class Meta:
        verbose_name_plural = "Tickets"

    def __str__(self):
        return f"[{self.get_status_ticket_suporte_display()}] {self.titulo}"


class TicketMensagem(models.Model):
    ticket = models.ForeignKey(
        "TicketSuporte",
        on_delete=models.CASCADE,
        related_name="mensagens",
        help_text="Ticket ao qual a mensagem pertence.",
    )
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        help_text="Usuário que escreveu a mensagem.",
    )
    conteudo = models.TextField(help_text="Conteúdo da mensagem enviada.")
    data_criacao = models.DateTimeField(
        auto_now_add=True, help_text="Data/hora em que a mensagem foi registrada."
    )

    class Meta:
        ordering = ["data_criacao"]

    def __str__(self):
        return f"Msg de {self.autor} em {self.data_criacao:%d/%m/%Y}"
