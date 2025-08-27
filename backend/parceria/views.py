from django.core.exceptions import ImproperlyConfigured
from django.http import Http404
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from .models import *
from .serializers import *


class BaseClienteViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        model = self.queryset.model

        if model == ContratoServico:
            return model.objects.filter(
                parceria__membros__user=user,
                parceria__membros__is_active=True
            )
        elif model == PedidoServico:
            return model.objects.filter(
                parceria__membros__user=user,
                parceria__membros__is_active=True
            )
        elif model == Pagamento:
            return model.objects.filter(
                pedido__parceria__membros__user=user,
                pedido__parceria__membros__is_active=True
            )
        else:
            raise ImproperlyConfigured(f"Queryset não configurado para {model.__name__}")

    def get_object(self):
        obj = super().get_object()
        user = self.request.user

        if hasattr(obj, "parceria"):
            if not obj.parceria.membros.filter(user=user, is_active=True).exists():
                raise Http404
        elif hasattr(obj, "pedido") and hasattr(obj.pedido, "parceria"):
            if not obj.pedido.parceria.membros.filter(user=user, is_active=True).exists():
                raise Http404
        else:
            raise PermissionDenied("Acesso negado.")

        return obj

    def perform_create(self, serializer):
        parceria = Parceria.objects.filter(
            membros__user=self.request.user,
            membros__is_active=True
        ).first()
        if not parceria:
            raise PermissionDenied("Usuário não está vinculado a uma parceria.")
        serializer.save(parceria=parceria)


class ServicoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Servico.objects.all()
    serializer_class = ServicoSerializer
    permission_classes = [permissions.IsAuthenticated]


class PedidoServicoViewSet(BaseClienteViewSet):
    queryset = PedidoServico.objects.all()
    serializer_class = PedidoServicoSerializer

    def destroy(self, request, *args, **kwargs):
        return Response(
            {'detail': 'Exclusão de pedidos não é permitida'},
            status=status.HTTP_403_FORBIDDEN
        )


class ContratoServicoViewSet(BaseClienteViewSet):
    queryset = ContratoServico.objects.all()
    serializer_class = ContratoServicoSerializer

    def destroy(self, request, *args, **kwargs):
        return Response(
            {'detail': 'Exclusão de contratos não é permitida'},
            status=status.HTTP_403_FORBIDDEN
        )


class PagamentoViewSet(BaseClienteViewSet):
    queryset = Pagamento.objects.all()
    serializer_class = PagamentoSerializer

    def get_queryset(self):
        user = self.request.user
        return Pagamento.objects.filter(
            pedido__parceria__proprietario=user
        ) | Pagamento.objects.filter(
            pedido__parceria__membros__user=user,
            pedido__parceria__membros__is_active=True
        )

    def destroy(self, request, *args, **kwargs):
        return Response(
            {'detail': 'Exclusão de pagamentos não é permitida'},
            status=status.HTTP_403_FORBIDDEN
        )


class PagamentoHistoricoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Histórico de alterações de status de pagamentos.
    Apenas leitura. Filtrado pela parceria do usuário via pagamento.pedido.
    """
    serializer_class = PagamentoHistoricoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return PagamentoHistorico.objects.filter(
            pagamento__pedido__parceria__membros__user=user,
            pagamento__pedido__parceria__membros__is_active=True
        ).distinct()

    def create(self, request, *args, **kwargs):
        return Response({'detail': 'Criação não permitida.'}, status=status.HTTP_403_FORBIDDEN)

    def update(self, request, *args, **kwargs):
        return Response({'detail': 'Edição não permitida.'}, status=status.HTTP_403_FORBIDDEN)

    def partial_update(self, request, *args, **kwargs):
        return Response({'detail': 'Edição não permitida.'}, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):
        return Response({'detail': 'Exclusão não permitida.'}, status=status.HTTP_403_FORBIDDEN)


class TicketSuporteViewSet(BaseClienteViewSet):
    queryset = TicketSuporte.objects.all()
    serializer_class = TicketSuporteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return TicketSuporte.objects.filter(
            parceria__proprietario=user
        ) | TicketSuporte.objects.filter(
            parceria__membros__user=user,
            parceria__membros__is_active=True
        )

    def perform_create(self, serializer):
        parceria = Parceria.objects.filter(
            proprietario=self.request.user
        ).first() or Parceria.objects.filter(
            membros__user=self.request.user,
            membros__is_active=True
        ).first()

        if not parceria:
            raise PermissionDenied("Usuário não está vinculado a uma parceria.")

        serializer.save(parceria=parceria)

    def destroy(self, request, *args, **kwargs):
        return Response(
            {'detail': 'Exclusão de Tickets não é permitida.'},
            status=status.HTTP_403_FORBIDDEN
        )
