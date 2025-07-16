from django.urls import reverse
from rest_framework import status
from django.utils import timezone

from parceria.models import (
    Parceria,
    Servico,
    PedidoServico,
    Pagamento,
    PagamentoHistorico,
)
from common.tests.test_utils import TestCaseUtils


class TestPagamentoHistoricoView(TestCaseUtils):
    """
    Testes para os endpoints de PagamentoHistorico.
    Garante que usuários só acessem históricos de seus próprios pagamentos.
    """

    def setUp(self):
        super().setUp()

        self.parceria1 = Parceria.objects.create(
            nome="A",
            tipo="cliente",
            user=self.user,
            nome_projeto="proj_a",
        )
        self.parceria2 = Parceria.objects.create(
            nome="B",
            tipo="cliente",
            user=self.user_b,
            nome_projeto="proj_b",
        )
        self.servico = Servico.objects.create(
            nome="Zola Site",
            preco=100,
            periodicidade="mensal",
        )
        self.pedido1 = PedidoServico.objects.create(
            parceria=self.parceria1,
            servico=self.servico,
        )
        self.pedido2 = PedidoServico.objects.create(
            parceria=self.parceria2,
            servico=self.servico,
        )
        self.pagamento1 = Pagamento.objects.create(
            pedido=self.pedido1,
            valor=100,
            status="pendente",
            metodo="pix",
        )
        self.pagamento2 = Pagamento.objects.create(
            pedido=self.pedido2,
            valor=100,
            status="pendente",
            metodo="boleto",
        )
        self.historico1 = PagamentoHistorico.objects.create(
            pagamento=self.pagamento1,
            status="pendente",
            detalhes={"msg": "Aguardando"},
        )
        self.historico2 = PagamentoHistorico.objects.create(
            pagamento=self.pagamento2,
            status="confirmado",
            detalhes={"msg": "Pago"},
        )

        self.list_url = reverse("parceria-pagamentohistorico-list")
        self.detail_url_1 = reverse("parceria-pagamentohistorico-detail", args=[self.historico1.id])
        self.detail_url_2 = reverse("parceria-pagamentohistorico-detail", args=[self.historico2.id])

    def test_list_retorna_apenas_historico_do_usuario(self):
        """GET /pagamentohistorico/ deve retornar apenas históricos da parceria do usuário autenticado."""
        response = self.auth_client.get(self.list_url)
        self.assertResponse200(response)
        ids = [h["id"] for h in response.data["results"]]
        self.assertIn(self.historico1.id, ids)
        self.assertNotIn(self.historico2.id, ids)

    def test_detail_de_outro_usuario_retorna_403(self):
        """GET /pagamentohistorico/{id}/ de outra parceria deve retornar 403."""
        response = self.auth_client.get(self.detail_url_2)
        self.assertResponse403(response)

    def test_criacao_nao_autorizada_retorna_403(self):
        """POST /pagamentohistorico/ não deve permitir criação via API."""
        payload = {
            "pagamento": self.pagamento1.id,
            "status": "confirmado",
            "detalhes": {"msg": "tentativa"},
        }
        response = self.auth_client.post(self.list_url, payload, format="json")
        self.assertResponse403(response)

    def test_patch_nao_autorizado_retorna_403(self):
        """PATCH /pagamentohistorico/{id}/ não deve permitir edição."""
        payload = {"status": "estornado"}
        response = self.auth_client.patch(self.detail_url_1, payload, format="json")
        self.assertResponse403(response)

    def test_delete_nao_autorizado_retorna_403(self):
        """DELETE /pagamentohistorico/{id}/ não deve permitir exclusão."""
        response = self.auth_client.delete(self.detail_url_1)
        self.assertResponse403(response)

    def test_usuario_nao_autenticado_bloqueado(self):
        """Usuário anônimo não pode acessar endpoints protegidos."""
        urls = [self.list_url, self.detail_url_1]
        for url in urls:
            response = self.client.get(url)
            self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
