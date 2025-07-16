from django.conf import settings
from django.db import models
from django.utils import timezone


class Servico(models.Model):
    PERIODICIDADE_CHOICES = [
        ('avulso', 'Avulso'),
        ('mensal', 'Mensal'),
        ('anual', 'Anual'),
    ]

    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    periodicidade = models.CharField(max_length=10, choices=PERIODICIDADE_CHOICES, default='avulso')

    def __str__(self):
        return self.nome


class Parceria(models.Model):
    TIPO_CHOICES = [
        ('cliente', 'Cliente'),
        ('marca', 'Marca'),
        ('conteudo', 'Criador de conteúdo'),
    ]

    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nome_projeto = models.CharField(max_length=100)
    dominio = models.CharField(max_length=100, blank=True, null=True)
    data_criacao = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.nome_projeto})"


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
    parceria = models.ForeignKey(Parceria, on_delete=models.CASCADE, related_name='pedidos')
    servico = models.ForeignKey(Servico, on_delete=models.PROTECT)
    data_pedido = models.DateTimeField(default=timezone.now)
    desconto = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    vencimento = models.DateTimeField(blank=True, null=True)
    contrato = models.ForeignKey(ContratoServico, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pendente', 'Pendente'),
            ('em_andamento', 'Em andamento'),
            ('concluido', 'Concluído'),
            ('cancelado', 'Cancelado'),
        ],
        default='pendente',
    )

    class Meta:
        verbose_name_plural = "Pedidos"


    def __str__(self):
        return f"{self.servico.nome} - {self.parceria.nome_projeto}"


class TicketSuporte(models.Model):
    TIPO_CHOICES = [
        ('sugestao', 'Sugestão de funcionalidade'),
        ('ajuda', 'Ajuda ou dúvida'),
        ('problema', 'Relato de problema'),
        ('outro', 'Outro'),
    ]

    STATUS_CHOICES = [
        ('novo', 'Novo'),
        ('em_analise', 'Em análise'),
        ('em_execucao', 'Em execução'),
        ('concluido', 'Concluído'),
        ('rejeitado', 'Rejeitado'),
    ]

    parceria = models.ForeignKey(Parceria, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    titulo = models.CharField(max_length=120)
    descricao = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='novo')
    data_criacao = models.DateTimeField(default=timezone.now)
    prazo_entrega = models.DateTimeField(blank=True, null=True)
    resposta = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Tickets"


    def __str__(self):
        return f"[{self.get_status_display()}] {self.titulo}"


class Pagamento(models.Model):
    METODO_CHOICES = [
        ('pix', 'Pix'),
        ('boleto', 'Boleto bancário'),
        ('crédito', 'Cartão de crédito'),
        ('débito', 'Cartão de débito'),
    ]
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('confirmado', 'Confirmado'),
        ('falhou', 'Falhou'),
        ('estornado', 'Estornado'),
    ]

    pedido = models.OneToOneField(PedidoServico, on_delete=models.CASCADE, related_name="pagamento")
    valor = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    metodo = models.CharField(max_length=30, choices=METODO_CHOICES)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.pedido} - {self.metodo} - {self.status}"


class PagamentoHistorico(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('confirmado', 'Confirmado'),
        ('falhou', 'Falhou'),
        ('estornado', 'Estornado'),
    ]

    pagamento = models.ForeignKey(Pagamento, on_delete=models.CASCADE, related_name="historico")
    status = models.CharField(max_length=20, choices=Pagamento.STATUS_CHOICES)
    detalhes = models.JSONField(blank=True, null=True)
    data = models.DateTimeField(auto_now_add=True)
