from .views import (
    ServicoViewSet,
    PedidoServicoViewSet,
    ContratoServicoViewSet,
    TicketSuporteViewSet,
)

routes = [
    {
        "regex": r"parceria/servicos",
        "viewset": ServicoViewSet,
        "basename": "parceria-servicos",
    },
    {
        "regex": r"parceria/pedidos",
        "viewset": PedidoServicoViewSet,
        "basename": "parceria-pedidos",
    },
    {
        "regex": r"parceria/contratos",
        "viewset": ContratoServicoViewSet,
        "basename": "parceria-contratos",
    },
    {
        "regex": r"parceria/tickets",
        "viewset": TicketSuporteViewSet,
        "basename": "parceria-tickets",
    },
]
