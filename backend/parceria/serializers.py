from rest_framework import serializers
from .models import Parceria, Servico, ContratoServico, PedidoServico, Pagamento, PagamentoHistorico, TicketSuporte


class ServicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servico
        fields = ['id', 'nome', 'descricao', 'periodicidade', 'preco']


class PedidoServicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PedidoServico
        fields = ['id', 'servico', 'contrato', 'status', 'data_pedido', 'desconto', 'vencimento']
        read_only_fields = ['data_pedido', 'status']


class ContratoServicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContratoServico
        fields = ['id', 'servico', 'data_inicio', 'data_fim', 'cancelado', 'observacoes']
        read_only_fields = ['data_inicio', 'data_fim', 'cancelado']


class PagamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pagamento
        fields = ['id', 'pedido', 'status', 'valor', 'metodo', 'criado_em']


class TicketSuporteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketSuporte
        fields = ['id', 'titulo', 'descricao', 'tipo', 'status', 'data_criacao']
