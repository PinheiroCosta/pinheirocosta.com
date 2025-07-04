from django.conf import settings
from django.db import models
from django.utils import timezone


class Servico(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    preco = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.nome


class Parceria(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nome_projeto = models.CharField(max_length=100)
    dominio = models.CharField(max_length=100, blank=True, null=True)
    data_criacao = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.nome_projeto})"


class PedidoServico(models.Model):
    parceria = models.ForeignKey(Parceria, on_delete=models.CASCADE, related_name='pedidos')
    servico = models.ForeignKey(Servico, on_delete=models.PROTECT)
    data_pedido = models.DateField(default=timezone.now)
    desconto = models.DecimalField(max_digits=2, decimal_places=0)
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
    vencimento = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.servico.nome} - {self.parceria.nome_projeto}"

class SugestaoServico(models.Model):
    parceria = models.ForeignKey(Parceria, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    data = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=[('nova', 'Nova'), ('avaliada', 'Avaliada')])

    def __str__(self):
        return f"{self.titulo} ({self.parceria})"
