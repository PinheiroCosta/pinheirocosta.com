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

        if model in [ContratoServico, PedidoServico]:
            return model.objects.filter(
                parceria__membros__usuario=user,
                parceria__membros__ativo=True
            )
        else:
            raise ImproperlyConfigured(f"Queryset não configurado para {model.__name__}")

    def get_object(self):
        obj = super().get_object()
        user = self.request.user

        if hasattr(obj, "parceria"):
            if not obj.parceria.membros.filter(usuario=user, ativo=True).exists():
                raise PermissionDenied("Acesso negado.")
        elif hasattr(obj, "pedido") and hasattr(obj.pedido, "parceria"):
            if not obj.pedido.parceria.membros.filter(usuario=user, ativo=True).exists():
                raise PermissionDenied("Acesso negado.")

        return obj

    def perform_create(self, serializer):
        parceria = Parceria.objects.filter(
            membros__usuario=self.request.user,
            membros__ativo=True
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

    def perform_create(self, serializer):
        parceria = Parceria.objects.filter(
            membros__usuario=self.request.user,
            membros__ativo=True
        ).first()
        if not parceria:
            raise PermissionDenied("Usuário não está vinculado a uma parceria.")
        pedido = serializer.save(parceria=parceria)

        # Cria itens se vierem no request
        itens_data = self.request.data.get("itens", [])
        for item_data in itens_data:
            servico_id = item_data.get("servico")
            cupom_id = item_data.get("cupom_promocional")
            recorrente = item_data.get("recorrente", False)
            periodo_gratuito = item_data.get("periodo_gratuito", 0)
            data_renovacao = item_data.get("data_renovacao")

            PedidoItem.objects.create(
                pedido=pedido,
                servico_id=servico_id,
                cupom_promocional_id=cupom_id,
                recorrente=recorrente,
                periodo_gratuito=periodo_gratuito,
                data_renovacao=data_renovacao
            )

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



class TicketSuporteViewSet(BaseClienteViewSet):
    queryset = TicketSuporte.objects.all()
    serializer_class = TicketSuporteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return TicketSuporte.objects.filter(
            parceria__proprietario=user
        ) | TicketSuporte.objects.filter(
            parceria__membros__usuario=user,
            parceria__membros__ativo=True
        )

    def perform_create(self, serializer):
        parceria = Parceria.objects.filter(
            proprietario=self.request.user
        ).first() or Parceria.objects.filter(
            membros__usuario=self.request.user,
            membros__ativo=True
        ).first()

        if not parceria:
            raise PermissionDenied("Usuário não está vinculado a uma parceria.")

        serializer.save(parceria=parceria)

    def destroy(self, request, *args, **kwargs):
        return Response(
            {'detail': 'Exclusão de Tickets não é permitida.'},
            status=status.HTTP_403_FORBIDDEN
        )


class CupomPromocionalViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CupomPromocional.objects.filter(ativo=True)
    serializer_class = CupomPromocionalSerializer
    permission_classes = [permissions.IsAuthenticated]
