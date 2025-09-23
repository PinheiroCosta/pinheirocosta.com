from django.conf import settings
from django.db import models
from django.utils import timezone


class BaseAtivoHistorico(models.Model):
    """
    Modelo abstrato para entidades com ciclo de vida (ativo, início, fim).
    """
    ativo = models.BooleanField(default=True)
    data_inicio = models.DateTimeField(default=timezone.now)
    data_fim = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True


class CupomPromocional(models.Model):
    """
    Representa um código promocional que pode ser aplicado a pedidos.
    
    - Pode oferecer desconto percentual ou valor fixo.
    - Pode ter validade (data de expiração).
    - Pode ser de uso único (uma vez aplicado, não pode ser reutilizado).
    """

    class TipoDesconto(models.TextChoices):
        PERCENTUAL = 'percentual', 'Percentual (%)'
        FIXO = 'fixo', 'Valor Fixo (R$)'

    cupom = models.CharField(max_length=50, unique=True)
    tipo = models.CharField(max_length=10, choices=TipoDesconto.choices)
    valor = models.DecimalField(max_digits=8, decimal_places=2)
    validade = models.DateTimeField(null=True, blank=True)
    ativo = models.BooleanField(default=True)
    uso_unico = models.BooleanField(default=False)

    data_criacao = models.DateTimeField(auto_now_add=True)
    data_uso = models.DateTimeField(null=True, blank=True, help_text="Data em que o código foi utilizado (para uso único).")

    def __str__(self):
        return self.cupom

    def aplicar_desconto(self, valor_original: float) -> float:
        """
        Retorna o valor após aplicar o desconto.
        Não altera o status do código; apenas calcula.
        """
        if not self.ativo:
            return valor_original
        if self.tipo == self.TipoDesconto.PERCENTUAL:
            return valor_original * (1 - float(self.valor) / 100)
        return max(valor_original - float(self.valor), 0)


class Servico(BaseAtivoHistorico):
    """
    Representa um serviço disponível no catálogo da plataforma.
    É a lista de opções que podem ser oferecidas aos clientes.
    Aqui ficam informações estáticas como nome, descrição, e preço base.
    """

    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    preco_base = models.DecimalField(max_digits=8, decimal_places=2)

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
        CLIENTE = 'cliente', 'Cliente'                  # parceiro que contrata os serviços/produtos do site.
        MARCA = 'marca', 'Marca'                        # empresas para co-marketing, licenciamento, divulgação.
        CONTEUDO = 'conteudo', 'Criador de conteúdo'    # criadores de conteúdo, influenciadores, afiliados.
        TECNOLOGIA = 'tecnologia', 'Tecnologia'         # integrações de API, provedores SaaS, hospedagem.
        FORNECEDOR = 'fornecedor', 'Fornecedor'         # parceiros que entregam insumos/serviços para nós
        DISTRIBUIDOR = 'distribuidor', 'Distribuidor'   # parceiros que levam o serviço a terceiros (marketplaces, revendedores).
        SOCIAL = 'social', 'Social'                     # iniciativas de impacto social ou cultural.
        COMUNIDADE = 'comunidade', 'Comunidade'         # grupos open source, fóruns, eventos.

    nome = models.CharField(max_length=100)
    natureza = models.CharField(max_length=2, choices=NaturezaParceria.choices)
    categoria = models.CharField(max_length=20, choices=CategoriaParceria.choices)
    proprietario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="parcerias_proprietario")
    dominio = models.CharField(max_length=100, blank=True, null=True)
    

    def __str__(self):
        return f"{self.nome} ({self.proprietario.get_full_name()})"


class ParceriaMembro(models.Model):
    """
    Usuários vinculados a uma parceria.
    Todo membro listado aqui é colaborador; o proprietário está definido em Parceria.proprietario.
    """

    parceria = models.ForeignKey(Parceria, on_delete=models.CASCADE, related_name="membros")
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="parcerias_membro")
    ativo = models.BooleanField(default=True)
    data_entrada = models.DateTimeField(default=timezone.now)

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

    parceria = models.ForeignKey(Parceria, on_delete=models.CASCADE, related_name='contratos')
    observacoes = models.TextField(blank=True)

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
        ContratoServico, on_delete=models.CASCADE, related_name="servicos_contratados"
    )
    servico = models.ForeignKey(
        Servico, on_delete=models.CASCADE, related_name="servicos_contratados"
    )
    recorrente = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.servico.nome} - Contrato de servico: ({self.contrato_servico.id}) "


class ContratoCobranca(models.Model):
    """
    Representa uma cobrança financeira associada a um serviço contratado.
    É a obrigação de pagamento do cliente para manter o serviço ativo.
    """

    servico_contratado = models.ForeignKey(
        ServicoContratado, on_delete=models.CASCADE, related_name="cobrancas"
    )
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    vencimento = models.DateField()
    data_pagamento = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Cobrança {self.valor} - {self.servico_contratado.servico.nome}"


class PedidoServico(BaseAtivoHistorico):
    """
    Intenção inicial do cliente: solicitação de um serviço.
    Pode ou não evoluir para um contrato formal.
    O status acompanha o ciclo do pedido (pendente → andamento → concluído/cancelado).
    """

    class PedidoServicoStatus(models.TextChoices):
        PENDENTE = 'pendente', 'Pendente'
        EM_ANDAMENTO = 'em_andamento', 'Em andamento'
        CONCLUIDO = 'concluido', 'Concluído'
        CANCELADO = 'cancelado', 'Cancelado'

    parceria = models.ForeignKey(Parceria, on_delete=models.CASCADE, related_name='pedidos')
    status_pedido_servico = models.CharField(
        max_length=20,
        choices=PedidoServicoStatus.choices,
        default=PedidoServicoStatus.PENDENTE,
    )

    class Meta:
        verbose_name_plural = "Pedidos"

    def __str__(self):
        return f"Pedido {self.id} - {self.parceria.nome}"


class PedidoItem(models.Model):
    """
    Item de um pedido de serviço. Permite que um pedido agrupe vários serviços.
    """

    pedido = models.ForeignKey(PedidoServico, on_delete=models.CASCADE, related_name="itens")
    servico = models.ForeignKey(Servico, on_delete=models.PROTECT)
    cupom_promocional = models.ForeignKey(
        CupomPromocional, on_delete=models.CASCADE, related_name="itens_promocionais", null=True, blank=True
    )
    data_renovacao = models.DateTimeField(blank=True, null=True)
    recorrente = models.BooleanField(default=False)
    periodo_gratuito = models.IntegerField(default=0, help_text="Número de meses gratuitos")


class TicketSuporte(models.Model):
    """
    Registro de solicitações de suporte abertas por clientes.
    Pode ser sugestão, dúvida, problema ou outro.
    Possui ciclo de vida (novo → análise → execução → concluído/rejeitado).
    """

    class TicketSuporteTipo(models.TextChoices):
        SUGESTAO = 'sugestao', 'Sugestão de funcionalidade'
        AJUDA = 'ajuda', 'Ajuda ou dúvida'
        PROBLEMA = 'problema', 'Relato de problema'
        OUTRO = 'outro', 'Outro'

    class TicketSuporteStatus(models.TextChoices):
        NOVO = 'novo', 'Novo'
        EM_ANALISE = 'em_analise', 'Em análise'
        EM_EXECUCAO = 'em_execucao', 'Em execução'
        CONCLUIDO = 'concluido', 'Concluído'
        REJEITADO = 'rejeitado', 'Rejeitado'

    parceria = models.ForeignKey(Parceria, on_delete=models.CASCADE)
    tipo_ticket_suporte = models.CharField(max_length=20, choices=TicketSuporteTipo.choices)
    titulo = models.CharField(max_length=120)
    descricao = models.TextField()
    status_ticket_suporte = models.CharField(max_length=20, choices=TicketSuporteStatus.choices, default=TicketSuporteStatus.NOVO)
    data_criacao = models.DateTimeField(auto_now_add=True)
    prazo_entrega = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Tickets"

    def __str__(self):
        return f"[{self.get_status_ticket_suporte_display()}] {self.titulo}"


class TicketMensagem(models.Model):
    ticket = models.ForeignKey("TicketSuporte", on_delete=models.CASCADE, related_name="mensagens")
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    conteudo = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["data_criacao"]

    def __str__(self):
        return f"Msg de {self.autor} em {self.data_criacao:%d/%m/%Y}"

