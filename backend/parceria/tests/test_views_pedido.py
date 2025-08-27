from django.utils import timezone
from common.tests.test_utils import TestCaseUtils
from parceria.models import PedidoServico, Servico, ContratoServico, Parceria, ParceriaMembro


class TestPedidoServicoView(TestCaseUtils):
    def setUp(self):
        super().setUp()
        self.view_url = "/api/parceria/pedidos/"
        
        self.parceria = Parceria.objects.create(
            nome="Cliente 1",
            tipo="cliente",
            proprietario=self.user,
            nome_projeto="site1",
            dominio="site1.com.br",
        )
        ParceriaMembro.objects.create(parceria=self.parceria, user=self.user, is_active=True)

        self.outro_parceiro = Parceria.objects.create(
            nome="Cliente 2",
            tipo="cliente",
            proprietario=self.user_b,
            nome_projeto="site2",
            dominio="site2.com.br",
        )
        ParceriaMembro.objects.create(parceria=self.outro_parceiro, user=self.user_b, is_active=True)

        self.servico = Servico.objects.create(
            nome="Site Zola",
            descricao="Criação de site estático",
            preco=500,
            periodicidade="avulso"
        )
        self.contrato = ContratoServico.objects.create(
            parceria=self.parceria,
            servico=self.servico
        )
        self.outro_contrato = ContratoServico.objects.create(
            parceria=self.outro_parceiro,
            servico=self.servico
        )

    def test_lista_pedidos_do_usuario(self):
        """Deve retornar apenas pedidos da parceria do usuário autenticado"""
        pedido = PedidoServico.objects.create(
            parceria=self.parceria,
            servico=self.servico,
            contrato=self.contrato,
            desconto=0,
            vencimento=timezone.now() + timezone.timedelta(days=30),
        )

        PedidoServico.objects.create(  # Outro usuário
            parceria=self.outro_parceiro,
            servico=self.servico,
            contrato=self.outro_contrato,
            desconto=0,
            vencimento=timezone.now() + timezone.timedelta(days=30),
        )

        resp = self.auth_client.get(self.view_url)
        self.assertResponse200(resp)
        ids = [p["id"] for p in resp.data['results']]
        self.assertIn(pedido.id, ids)
        self.assertEqual(resp.data["count"], 1)
        self.assertEqual(len(resp.data["results"]), 1)

    def test_criacao_pedido_valido(self):
        """Deve permitir criação de pedido vinculado a contrato da parceria do usuário"""
        payload = {
            "contrato": self.contrato.id,
            "servico": self.servico.id,
            "desconto": "0.00",
            "vencimento": "2099-12-31T12:00:00Z",
        }
        resp = self.auth_client.post(self.view_url, payload, format="json")
        self.assertResponse201(resp)

    def test_criacao_pedido_contrato_de_terceiro(self):
        """Não deve permitir criação de pedido com contrato de outro usuário"""
        payload = {
            "contrato": self.outro_contrato.id,
            "servico": self.outro_contrato.servico.id,
            "desconto": "0.00",
            "vencimento": "2099-12-31T12:00:00Z",
        }
        resp = self.auth_client.post(self.view_url, payload, format="json")
        self.assertResponse403(resp)

    def test_detalhe_pedido_outro_usuario(self):
        """Usuário não deve acessar pedido de outro parceiro"""
        outro_pedido = PedidoServico.objects.create(
            parceria=self.outro_parceiro,
            servico=self.servico,
            contrato=self.outro_contrato,
            desconto=0,
            vencimento=timezone.now() + timezone.timedelta(days=30),
        )
        url = f"/api/parceria/pedidos/{outro_pedido.id}/"
        resp = self.auth_client.get(url)
        self.assertResponse404(resp)

    def test_delete_pedido_bloqueado(self):
        """DELETE não deve ser permitido"""
        pedido = PedidoServico.objects.create(
            parceria=self.parceria,
            servico=self.servico,
            contrato=self.contrato,
            desconto=0,
            vencimento=timezone.now() + timezone.timedelta(days=30),
        )
        url = f"/api/parceria/pedidos/{pedido.id}/"
        resp = self.auth_client.delete(url)
        self.assertResponse403(resp)
