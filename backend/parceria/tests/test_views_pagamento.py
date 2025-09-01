from django.utils import timezone
from django.urls import reverse
from rest_framework import status

from parceria.models import (
    Pagamento,
    PagamentoHistorico,
    PedidoServico,
    Servico,
    Parceria,
)
from common.tests.test_utils import TestCaseUtils


class TestPagamentoView(TestCaseUtils):
    """
    Testes para os endpoints de Pagamento. Garante que o usuário autenticado
    possa interagir apenas com os pagamentos da sua parceria.
    """

    def setUp(self):
        super().setUp()

        # Parcerias
        self.parceria1 = Parceria.objects.create(
            nome="Parceria A",
            tipo_parceria="cliente",
            proprietario=self.user,
            nome_projeto="proj_a",
        )
        self.parceria2 = Parceria.objects.create(
            nome="Parceria B",
            tipo_parceria="cliente",
            proprietario=self.user_b,
            nome_projeto="proj_b",
        )

        # Serviço
        self.servico = Servico.objects.create(
            nome="Site Profissional",
            preco=200,
            periodicidade_servico="mensal",
        )

        # Pedidos
        self.pedido1 = PedidoServico.objects.create(parceria=self.parceria1, servico=self.servico, status_pedido_servico="pendente")
        self.pedido2 = PedidoServico.objects.create(parceria=self.parceria2, servico=self.servico, status_pedido_servico="pendente")

        # Pagamentos
        self.pagamento1 = Pagamento.objects.create(pedido=self.pedido1, valor=200, status_pagamento="pendente", metodo_pagamento="pix")
        self.pagamento2 = Pagamento.objects.create(pedido=self.pedido2, valor=200, status_pagamento="pendente", metodo_pagamento="boleto")

        # URLs
        self.list_url = reverse("parceria-pagamentos-list")
        self.detail_url_1 = reverse("parceria-pagamentos-detail", args=[self.pagamento1.id])
        self.detail_url_2 = reverse("parceria-pagamentos-detail", args=[self.pagamento2.id])

    def test_list_retorna_pagamentos_do_usuario(self):
        """GET /pagamentos/ deve retornar apenas pagamentos da parceria do usuário autenticado."""
        response = self.auth_client.get(self.list_url)
        self.assertResponse200(response)
        ids = [item["id"] for item in response.data["results"]]
        self.assertIn(self.pagamento1.id, ids)
        self.assertNotIn(self.pagamento2.id, ids)

    def test_detail_pagamento_de_outra_parceria_retorna_404(self):
        """GET /pagamentos/{id}/ de outra parceria deve retornar 404."""
        response = self.auth_client.get(self.detail_url_2)
        self.assertResponse404(response)

    def test_update_pagamento_de_outra_parceria_retorna_404(self):
        """PATCH /pagamentos/{id}/ de outra parceria deve retornar 404."""
        payload = {"status_pagamento": "confirmado"}
        response = self.auth_client.patch(self.detail_url_2, payload, format="json")
        self.assertResponse404(response)

    def test_delete_pagamento_de_outra_parceria_retorna_403(self):
        """DELETE /pagamentos/{id}/ de outra parceria deve retornar 403."""
        response = self.auth_client.delete(self.detail_url_2)
        self.assertResponse403(response)

    def test_usuario_nao_autenticado_nao_pode_acessar(self):
        """Usuário anônimo não pode acessar endpoints protegidos."""
        urls = [self.list_url, self.detail_url_1]
        for url in urls:
            response = self.client.get(url)
            self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
