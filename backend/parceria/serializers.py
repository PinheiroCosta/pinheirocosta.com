from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from .models import Parceria, Servico, ContratoServico, PedidoServico, TicketSuporte, PedidoItem, CupomPromocional, ServicoContratado


class CupomPromocionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = CupomPromocional
        fields = ['id', 'cupom', 'tipo', 'valor', 'validade', 'ativo', 'uso_unico', 'data_uso']


class ServicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servico
        fields = ['id', 'nome', 'descricao', 'preco_base']


class PedidoItemSerializer(serializers.ModelSerializer):
    servico = ServicoSerializer(read_only=True)
    cupom_promocional = CupomPromocionalSerializer(read_only=True)
    
    class Meta:
        model = PedidoItem
        fields = ['id', 'servico', 'cupom_promocional', 'data_renovacao', 'recorrente', 'periodo_gratuito']


class ServicoContratadoSerializer(serializers.ModelSerializer):
    servico = ServicoSerializer(read_only=True)
    cupom_promocional = CupomPromocionalSerializer(read_only=True)

    class Meta:
        model = ServicoContratado
        fields = ['id', 'servico', 'cupom_promocional', 'data_inicio', 'data_fim', 'recorrente']


class PedidoServicoSerializer(serializers.ModelSerializer):
    itens = PedidoItemSerializer(many=True, read_only=True)

    class Meta:
        model = PedidoServico
        fields = ['id', 'parceria', 'status_pedido_servico', 'itens']
        read_only_fields = ['status_pedido_servico']

    def create(self, validated_data):
        user = self.context["request"].user
        try:
            parceria = Parceria.objects.get(proprietario=user)
        except Parceria.DoesNotExist:
            raise PermissionDenied("Usuário não está vinculado a uma parceria.")
        if contrato.parceria != parceria:
            raise PermissionDenied("Contrato não pertence à sua parceria.")
        return super().create({**validated_data, "parceria": parceria})


class ContratoServicoSerializer(serializers.ModelSerializer):
    servicos_contratados = ServicoContratadoSerializer(many=True, read_only=True)

    class Meta:
        model = ContratoServico
        fields = ['id', 'parceria', 'data_inicio', 'data_fim', 'ativo', 'observacoes', 'servicos_contratados']
        read_only_fields = ['parceria', 'data_inicio', 'ativo']

    def create(self, validated_data):
        user = self.context["request"].user
        try:
            parceria = Parceria.objects.get(membros__usuario=user, membros__ativo=True)
        except Parceria.DoesNotExist:
            raise PermissionDenied("Usuário não está vinculado a uma parceria.")
        return super().create({**validated_data, "parceria": parceria})


class TicketSuporteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketSuporte
        fields = ['id', 'titulo', 'descricao', 'tipo_ticket_suporte', 'status_ticket_suporte', 'data_criacao', 'prazo_entrega']
        read_only_fields = ['status_ticket_suporte', 'data_criacao']
