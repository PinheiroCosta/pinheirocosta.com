from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ServicoViewSet,
    PedidoServicoViewSet,
    ContratoServicoViewSet,
    PagamentoViewSet,
    TicketSuporteViewSet,
)

router = DefaultRouter()
router.register("servicos", ServicoViewSet, basename="servicos")
router.register("pedidos", PedidoServicoViewSet, basename="pedidos")
router.register("contratos", ContratoServicoViewSet, basename="contratos")
router.register("pagamentos", PagamentoViewSet, basename="pagamentos")
router.register("tickets", TicketSuporteViewSet, basename="tickets")

urlpatterns = [
    path("", include(router.urls)),
]

