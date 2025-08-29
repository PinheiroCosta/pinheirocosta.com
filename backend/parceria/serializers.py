from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from .models import Parceria, Servico, ContratoServico, PedidoServico, Pagamento, PagamentoHistorico, TicketSuporte


class ServicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servico
        fields = ['id', 'nome', 'descricao', 'periodicidade_servico', 'preco']


class PedidoServicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PedidoServico
        fields = ['id', 'servico', 'contrato', 'status_pedido_servico', 'data_pedido', 'desconto', 'vencimento']
        read_only_fields = ['data_pedido', 'status_pedido_servico']

    def create(self, validated_data):
        contrato = validated_data["contrato"]
        user = self.context["request"].user
        try:
            parceria = Parceria.objects.get(proprietario=user)
        except Parceria.DoesNotExist:
            raise PermissionDenied("Usuário não está vinculado a uma parceria.")
        if contrato.parceria != parceria:
            raise PermissionDenied("Contrato não pertence à sua parceria.")
        return super().create(validated_data)


class ContratoServicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContratoServico
        fields = ['id', 'servico', 'parceria', 'data_inicio', 'data_fim', 'cancelado', 'observacoes']
        read_only_fields = ['parceria', 'data_inicio', 'data_fim', 'cancelado']

    def create(self, validated_data):
        user = self.context["request"].user
        try:
            parceria = Parceria.objects.get(membros__user=user, membros__is_active=True)
        except Parceria.DoesNotExist:
            raise PermissionDenied("Usuário não está vinculado a uma parceria.")
        return super().create({**validated_data, "parceria": parceria})


class PagamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pagamento
        fields = ['id', 'pedido', 'status_pagamento', 'valor', 'metodo_pagamento', 'criado_em', 'atualizado_em']


class PagamentoHistoricoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PagamentoHistorico
        fields = ['id', 'pagamento', 'status_historico_pagamento', 'detalhes', 'data']
        read_only_fields = fields


class TicketSuporteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketSuporte
        fields = ['id', 'titulo', 'descricao', 'tipo_ticket_suporte', 'status_ticket_suporte', 'data_criacao']
        read_only_fields = ['status', 'data_criacao']
