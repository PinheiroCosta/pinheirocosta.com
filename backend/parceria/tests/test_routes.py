from common.tests.test_utils import TestCaseUtils
from django.urls import resolve


class TestParceriaRoutes(TestCaseUtils):
    """
    Verifica se as principais rotas da API de parceria estão corretamente registradas no Django.
    """

    def test_parceria_routes_exist(self):
        """
        Garante que todas as rotas esperadas da API de parceria possam ser resolvidas sem erro.
        """
        expected_routes = [
            "/api/parceria/servicos/",
            "/api/parceria/pedidos/",
            "/api/parceria/contratos/",
            "/api/parceria/tickets/",
        ]

        for route in expected_routes:
            try:
                resolver = resolve(route)
                self.assertIsNotNone(resolver.func, f"Rota não encontrada: {route}")
            except Exception:
                self.fail(f"Rota inválida ou não registrada: {route}")
