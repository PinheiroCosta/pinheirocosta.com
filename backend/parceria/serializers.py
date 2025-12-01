from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from .models import Parceria, Servico, ContratoServico, PedidoServico, TicketSuporte, PedidoItem, ServicoContratado


class ServicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servico
        fields = ['id', 'nome', 'descricao', 'preco_base']


class PedidoItemSerializer(serializers.ModelSerializer):
    servico = ServicoSerializer(read_only=True)

    class Meta:
        model = PedidoItem
        fields = ['id', 'servico', 'data_renovacao', 'recorrente']


class ServicoContratadoSerializer(serializers.ModelSerializer):
    servico = ServicoSerializer(read_only=True)

    class Meta:
        model = ServicoContratado
        fields = ['id', 'servico', 'data_inicio', 'data_fim', 'recorrente']


class PedidoServicoSerializer(serializers.ModelSerializer):
    itens = PedidoItemSerializer(many=True, read_only=True)

    class Meta:
        model = PedidoServico
        fields = ['id', 'parceria', 'status_pedido_servico', 'itens']
        read_only_fields = ['parceria', 'status_pedido_servico']


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
    tipo_ticket_suporte = serializers.CharField(required=False, allow_null=True)

    class Meta:
        model = TicketSuporte
        fields = ['id', 'titulo', 'descricao', 'tipo_ticket_suporte', 'status_ticket_suporte', 'data_criacao', 'prazo_entrega']
        read_only_fields = ['status_ticket_suporte', 'data_criacao']
