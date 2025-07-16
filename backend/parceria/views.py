from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from .models import *
from .serializers import *


class BaseClienteViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        if obj.parceria.user != self.request.user:
            raise PermissionDenied()
        return obj

    def get_queryset(self):
        return self.queryset.filter(parceria__user=self.request.user)

    def perform_create(self, serializer):
        parceria = Parceria.objects.get(user=self.request.user)
        serializer.save(parceria=parceria)


class ServicoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Servico.objects.all()
    serializer_class = ServicoSerializer
    permission_classes = [permissions.IsAuthenticated]


class PedidoServicoViewSet(BaseClienteViewSet):
    queryset = PedidoServico.objects.all()
    serializer_class = PedidoServicoSerializer


class ContratoServicoViewSet(BaseClienteViewSet):
    queryset = ContratoServico.objects.all()
    serializer_class = ContratoServicoSerializer


class PagamentoViewSet(BaseClienteViewSet):
    queryset = Pagamento.objects.all()
    serializer_class = PagamentoSerializer

    def get_queryset(self):
        return self.queryset.filter(pedido__parceria__user=self.request.user)


class PagamentoHistoricoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Histórico de alterações de status de pagamentos.
    Apenas leitura. Filtrado pela parceria do usuário via pagamento.pedido.
    """
    serializer_class = PagamentoHistoricoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not hasattr(user, "parceria"):
            raise PermissionDenied("Usuário não está vinculado a uma parceria.")
    
        return PagamentoHistorico.objects.filter(
            pagamento__pedido__parceria=user_parceria
        )


class TicketSuporteViewSet(BaseClienteViewSet):
    queryset = TicketSuporte.objects.all()
    serializer_class = TicketSuporteSerializer
