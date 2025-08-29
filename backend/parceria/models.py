from django.conf import settings
from django.db import models
from django.utils import timezone


class Servico(models.Model):
    class ServicoPeriodicidade(models.TextChoices):
        AVULSO = 'avulso', 'Avulso'
        MENSAL = 'mensal', 'Mensal'
        ANUAL = 'anual', 'Anual'

    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    periodicidade = models.CharField(max_length=10, choices=ServicoPeriodicidade.choices, default=ServicoPeriodicidade.AVULSO)

    def __str__(self):
        return self.nome


class Parceria(models.Model):
    class ParceriaTipo(models.TextChoices):
        CLIENTE = 'cliente', 'Cliente'
        MARCA = 'marca', 'Marca'
        CONTEUDO = 'conteudo', 'Criador de conteúdo'

    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=ParceriaTipo.choices)
    proprietario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="parcerias_proprietario")
    nome_projeto = models.CharField(max_length=100)
    dominio = models.CharField(max_length=100, blank=True, null=True)
    data_criacao = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.nome_projeto} ({self.proprietario.get_full_name()})"


class ParceriaMembro(models.Model):
    class ParceriaMembroRole(models.TextChoices):
        PROPRIETARIO = 'proprietario', 'Proprietario'
        COLABORADOR = 'colaborador', 'Colaborador'

    parceria = models.ForeignKey(Parceria, on_delete=models.CASCADE, related_name="membros")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="parcerias_membro")
    role = models.CharField(max_length=20, choices=ParceriaMembroRole.choices, default=ParceriaMembroRole.COLABORADOR)
    is_active = models.BooleanField(default=True)
    data_entrada = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("parceria", "user")
        verbose_name = "Membro de Parceria"
        verbose_name_plural = "Membros de Parceria"

    def __str__(self):
        return f"{self.user.get_username()} em {self.parceria.nome_projeto} ({self.role})"


class ContratoServico(models.Model):
    parceria = models.ForeignKey(Parceria, on_delete=models.CASCADE, related_name='contratos')
    servico = models.ForeignKey(Servico, on_delete=models.PROTECT)
    data_inicio = models.DateTimeField(default=timezone.now)
    data_fim = models.DateTimeField(blank=True, null=True)
    cancelado = models.BooleanField(default=False)
    observacoes = models.TextField(blank=True)

    class Meta:
        unique_together = ('parceria', 'servico', 'data_inicio')
        verbose_name = "Contrato de Serviço"
        verbose_name_plural = "Contratos de Serviço"

    def __str__(self):
        return f"{self.parceria} - {self.servico} ({self.data_inicio})"


class PedidoServico(models.Model):
    class PedidoServicoStatus(models.TextChoices):
        PENDENTE = 'pendente', 'Pendente'
        EM_ANDAMENTO = 'em_andamento', 'Em andamento'
        CONCLUIDO = 'concluido', 'Concluído'
        CANCELADO = 'cancelado', 'Cancelado'

    parceria = models.ForeignKey(Parceria, on_delete=models.CASCADE, related_name='pedidos')
    servico = models.ForeignKey(Servico, on_delete=models.PROTECT)
    data_pedido = models.DateTimeField(default=timezone.now)
    desconto = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    vencimento = models.DateTimeField(blank=True, null=True)
    contrato = models.ForeignKey(ContratoServico, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=PedidoServicoStatus.choices,
        default=PedidoServicoStatus.PENDENTE,
    )

    class Meta:
        verbose_name_plural = "Pedidos"

    def __str__(self):
        return f"{self.servico.nome} - {self.parceria.nome_projeto}"


class TicketSuporte(models.Model):
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
    tipo = models.CharField(max_length=20, choices=TicketSuporteTipo.choices)
    titulo = models.CharField(max_length=120)
    descricao = models.TextField()
    status = models.CharField(max_length=20, choices=TicketSuporteStatus.choices, default=TicketSuporteStatus.NOVO)
    data_criacao = models.DateTimeField(default=timezone.now)
    prazo_entrega = models.DateTimeField(blank=True, null=True)
    resposta = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Tickets"

    def __str__(self):
        return f"[{self.get_status_display()}] {self.titulo}"


class Pagamento(models.Model):
    class PagamentoMetodo(models.TextChoices):
        PIX = 'pix', 'Pix'
        BOLETO = 'boleto', 'Boleto bancário'
        CREDITO = 'crédito', 'Cartão de crédito'
        DEBITO = 'débito', 'Cartão de débito'

    class PagamentoStatus(models.TextChoices):
        PENDENTE = 'pendente', 'Pendente'
        CONFIRMADO = 'confirmado', 'Confirmado'
        FALHOU = 'falhou', 'Falhou'
        ESTORNADO = 'estornado', 'Estornado'

    pedido = models.OneToOneField(PedidoServico, on_delete=models.CASCADE, related_name="pagamento")
    valor = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20, choices=PagamentoStatus.choices, default=PagamentoStatus.PENDENTE)
    metodo = models.CharField(max_length=30, choices=PagamentoMetodo.choices)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.pedido} - {self.metodo} - {self.status}"


class PagamentoHistorico(models.Model):
    class PagamentoHistoricoStatus(models.TextChoices):
        PENDENTE = 'pendente', 'Pendente'
        CONFIRMADO = 'confirmado', 'Confirmado'
        FALHOU = 'falhou', 'Falhou'
        ESTORNADO = 'estornado', 'Estornado'

    pagamento = models.ForeignKey(Pagamento, on_delete=models.CASCADE, related_name="historico")
    status = models.CharField(max_length=20, choices=PagamentoHistoricoStatus.choices)
    detalhes = models.JSONField(blank=True, null=True)
    data = models.DateTimeField(auto_now_add=True)
