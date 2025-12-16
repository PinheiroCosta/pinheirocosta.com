from django.utils import timezone
from common.tests.test_utils import TestCaseUtils
from parceria.models import PedidoServico, PedidoItem, Servico, ContratoServico, Parceria, ParceriaMembro


class TestPedidoServicoView(TestCaseUtils):
    def setUp(self):
        super().setUp()
        self.view_url = "/api/parceria/pedidos/"

        self.parceria = Parceria.objects.create(
            nome="Cliente 1",
            natureza="pf",
            categoria="cliente",
            proprietario=self.user,
            dominio="site1.com.br",
        )
        ParceriaMembro.objects.create(parceria=self.parceria, usuario=self.user, ativo=True)

        self.outro_parceiro = Parceria.objects.create(
            nome="Cliente 2",
            natureza="pf",
            categoria="cliente",
            proprietario=self.user_b,
            dominio="site2.com.br",
        )
        ParceriaMembro.objects.create(parceria=self.outro_parceiro, usuario=self.user_b, ativo=True)

        self.servico = Servico.objects.create(
            nome="Site Zola",
            descricao="Criação de site estático",
            preco_base=500,
        )
        self.contrato = ContratoServico.objects.create(
            parceria=self.parceria,
            observacoes="Criado pela Suite de testes"
        )
        self.outro_contrato = ContratoServico.objects.create(
            parceria=self.outro_parceiro,
            observacoes="criado pela suite de testes"
        )

    def test_lista_pedidos_do_usuario(self):
        """Deve retornar apenas pedidos da parceria do usuário autenticado"""
        pedido = PedidoServico.objects.create(
            parceria=self.parceria,
            status_pedido_servico="pendente",
        )

        PedidoServico.objects.create(  # Outro usuário
            parceria=self.outro_parceiro,
            status_pedido_servico="pendente",
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
            "itens": [
                {"servico": self.servico.id}
            ]
        }
        resp = self.auth_client.post(
            self.view_url,
            payload,
            format="json",
            HTTP_IDEMPOTENCY_KEY="pedido-valido-1"
        )
        self.assertResponse201(resp)

        # validações extras mínimas
        pedido_id = resp.data.get("id")
        self.assertIsNotNone(pedido_id)
        pedido = PedidoServico.objects.get(id=pedido_id)
        self.assertEqual(pedido.parceria.id, self.parceria.id)
        self.assertEqual(pedido.itens.count(), 1)
        self.assertEqual(pedido.itens.first().servico.id, self.servico.id)

    def test_criacao_pedido_contrato_de_terceiro(self):
        """Não deve permitir criação de pedido com contrato de outro usuário"""
        # remove vínculo do usuário (desativa o membro)
        ParceriaMembro.objects.filter(parceria=self.parceria, usuario=self.user).update(ativo=False)

        payload = {
            "itens": [
                {"servico": self.servico.id}
            ]
        }
        resp = self.auth_client.post(
            self.view_url,
            payload,
            format="json",
            HTTP_IDEMPOTENCY_KEY="pedido-terceiro-1"
        )
        self.assertResponse403(resp)

    def test_detalhe_pedido_outro_usuario(self):
        """Usuário não deve acessar pedido de outro parceiro"""
        outro_pedido = PedidoServico.objects.create(
            parceria=self.outro_parceiro,
            status_pedido_servico="pendente",
        )
        url = f"/api/parceria/pedidos/{outro_pedido.id}/"
        resp = self.auth_client.get(url)
        self.assertResponse404(resp)

    def test_delete_pedido_bloqueado(self):
        """DELETE não deve ser permitido"""
        pedido = PedidoServico.objects.create(
            parceria=self.parceria,
            status_pedido_servico="pendente",
        )
        url = f"/api/parceria/pedidos/{pedido.id}/"
        resp = self.auth_client.delete(url)
        self.assertResponse403(resp)

    # ------------------------------------------------------------------------
    # /api/parceria/pedidos/{pedido.id}/concluir/
    # ------------------------------------------------------------------------
    def test_concluir_pedido_em_andamento(self):
        """Deve concluir pedido em andamento e retornar dados atualizados"""
        pedido = PedidoServico.objects.create(
            parceria=self.parceria,
            status_pedido_servico=PedidoServico.PedidoServicoStatus.EM_ANDAMENTO,
        )
        PedidoItem.objects.create(pedido=pedido, servico=self.servico)

        url = f"/api/parceria/pedidos/{pedido.id}/concluir/"
        resp = self.auth_client.post(url)

        self.assertResponse200(resp)
        pedido.refresh_from_db()
        self.assertEqual(pedido.status_pedido_servico, PedidoServico.PedidoServicoStatus.CONCLUIDO)
        self.assertIsNotNone(pedido.data_fim)

    def test_concluir_pedido_pendente(self):
        """Pedidos pendentes não devem ser concluídos"""
        pedido = PedidoServico.objects.create(
            parceria=self.parceria,
            status_pedido_servico=PedidoServico.PedidoServicoStatus.PENDENTE,
        )
        PedidoItem.objects.create(pedido=pedido, servico=self.servico)

        url = f"/api/parceria/pedidos/{pedido.id}/concluir/"
        resp = self.auth_client.post(url)

        self.assertResponse400(resp)
        pedido.refresh_from_db()
        self.assertEqual(pedido.status_pedido_servico, PedidoServico.PedidoServicoStatus.PENDENTE)

    def test_concluir_pedido_ja_concluido(self):
        """Pedido já concluído não pode ser concluído novamente"""
        pedido = PedidoServico.objects.create(
            parceria=self.parceria,
            status_pedido_servico=PedidoServico.PedidoServicoStatus.CONCLUIDO,
        )
        PedidoItem.objects.create(pedido=pedido, servico=self.servico)

        url = f"/api/parceria/pedidos/{pedido.id}/concluir/"
        resp = self.auth_client.post(url)

        self.assertResponse400(resp)

    def test_concluir_pedido_sem_itens(self):
        """Pedido sem itens não pode ser concluído"""
        pedido = PedidoServico.objects.create(
            parceria=self.parceria,
            status_pedido_servico=PedidoServico.PedidoServicoStatus.EM_ANDAMENTO,
        )

        url = f"/api/parceria/pedidos/{pedido.id}/concluir/"
        resp = self.auth_client.post(url)

        self.assertResponse400(resp)

    def test_concluir_item_recorrente_sem_data_renovacao(self):
        """Itens recorrentes exigem data de renovação"""
        pedido = PedidoServico.objects.create(
            parceria=self.parceria,
            status_pedido_servico=PedidoServico.PedidoServicoStatus.EM_ANDAMENTO,
        )
        PedidoItem.objects.create(
            pedido=pedido,
            servico=self.servico,
            recorrente=True,
            data_renovacao=None,
        )

        url = f"/api/parceria/pedidos/{pedido.id}/concluir/"
        resp = self.auth_client.post(url)

        self.assertResponse400(resp)

    def test_concluir_pedido_outro_usuario(self):
        """Usuário não deve concluir pedido de outra parceria"""
        pedido = PedidoServico.objects.create(
            parceria=self.outro_parceiro,
            status_pedido_servico=PedidoServico.PedidoServicoStatus.EM_ANDAMENTO,
        )
        PedidoItem.objects.create(pedido=pedido, servico=self.servico)

        url = f"/api/parceria/pedidos/{pedido.id}/concluir/"
        resp = self.auth_client.post(url)

        self.assertResponse404(resp)

    def test_concluir_pedido_servico_inativo(self):
        """Serviço inativo em item deve impedir conclusão"""
        servico_inativo = Servico.objects.create(
            nome="X",
            preco_base=100,
            ativo=False
        )

        pedido = PedidoServico.objects.create(
            parceria=self.parceria,
            status_pedido_servico=PedidoServico.PedidoServicoStatus.EM_ANDAMENTO,
        )
        PedidoItem.objects.create(pedido=pedido, servico=servico_inativo)

        url = f"/api/parceria/pedidos/{pedido.id}/concluir/"
        resp = self.auth_client.post(url)

        self.assertResponse400(resp)

    def test_concluir_pedido_atomicidade(self):
        """Falha na validação não deve alterar status nem registrar data"""
        pedido = PedidoServico.objects.create(
            parceria=self.parceria,
            status_pedido_servico=PedidoServico.PedidoServicoStatus.EM_ANDAMENTO,
        )
        # item inválido → recorrente sem data
        PedidoItem.objects.create(
            pedido=pedido,
            servico=self.servico,
            recorrente=True,
            data_renovacao=None,
        )

        url = f"/api/parceria/pedidos/{pedido.id}/concluir/"
        resp = self.auth_client.post(url)
        self.assertResponse400(resp)

        pedido.refresh_from_db()
        self.assertEqual(pedido.status_pedido_servico, PedidoServico.PedidoServicoStatus.EM_ANDAMENTO)
        self.assertIsNone(pedido.data_fim)

    # ------------------------------------------------------------------------
    # /api/parceria/pedidos/{pedido.id}/cancelar/
    # ------------------------------------------------------------------------

    def test_cancelar_pedido_em_andamento(self):
        """Deve cancelar pedido EM_ANDAMENTO e registrar data_fim"""
        pedido = PedidoServico.objects.create(
            parceria=self.parceria,
            status_pedido_servico=PedidoServico.PedidoServicoStatus.EM_ANDAMENTO
        )
        PedidoItem.objects.create(
            pedido=pedido,
            servico=self.servico,
            recorrente=False,
            data_renovacao=None,
        )

        url = f"/api/parceria/pedidos/{pedido.id}/cancelar/"
        resp = self.auth_client.post(url)
        self.assertResponse200(resp)

        pedido.refresh_from_db()
        self.assertEqual(pedido.status_pedido_servico, PedidoServico.PedidoServicoStatus.CANCELADO)
        self.assertIsNotNone(pedido.data_fim)

    def test_cancelar_pedido_pendente(self):
        """Deve cancelar pedido pendente"""
        pedido = PedidoServico.objects.create(
            parceria=self.parceria,
            status_pedido_servico=PedidoServico.PedidoServicoStatus.PENDENTE
        )
        PedidoItem.objects.create(
            pedido=pedido,
            servico=self.servico,
            recorrente=False,
            data_renovacao=None,
        )

        url = f"/api/parceria/pedidos/{pedido.id}/cancelar/"
        resp = self.auth_client.post(url)
        self.assertResponse200(resp)

        pedido.refresh_from_db()
        self.assertEqual(pedido.status_pedido_servico, PedidoServico.PedidoServicoStatus.CANCELADO)
        self.assertIsNotNone(pedido.data_fim)


    def test_cancelar_pedido_ja_cancelado(self):
        """Pedido já cancelado não deve ser cancelado novamente"""
        pedido = PedidoServico.objects.create(
            parceria=self.parceria,
            status_pedido_servico=PedidoServico.PedidoServicoStatus.CANCELADO
        )
        PedidoItem.objects.create(
            pedido=pedido,
            servico=self.servico,
            recorrente=False,
            data_renovacao=None,
        )

        url = f"/api/parceria/pedidos/{pedido.id}/cancelar/"
        resp = self.auth_client.post(url)
        self.assertResponse400(resp)

        pedido.refresh_from_db()
        self.assertEqual(pedido.status_pedido_servico, PedidoServico.PedidoServicoStatus.CANCELADO)


    def test_cancelar_pedido_outro_usuario(self):
        """Usuário não deve cancelar pedido de outra parceria"""
        pedido = PedidoServico.objects.create(
            parceria=self.outro_parceiro,
            status_pedido_servico=PedidoServico.PedidoServicoStatus.PENDENTE,
        )
        PedidoItem.objects.create(
            pedido=pedido,
            servico=self.servico,
            recorrente=True,
        )

        url = f"/api/parceria/pedidos/{pedido.id}/cancelar/"
        resp = self.auth_client.post(url)

        self.assertResponse404(resp)

        pedido.refresh_from_db()
        self.assertEqual(pedido.status_pedido_servico, PedidoServico.PedidoServicoStatus.PENDENTE)
        self.assertIsNone(pedido.data_fim)

    def test_cancelar_pedido_atomicidade(self):
        """Falha deve manter status original e não registrar data_fim"""
        pedido = PedidoServico.objects.create(
            parceria=self.parceria,
            # item inválido → pedido CONCLUIDO
            status_pedido_servico=PedidoServico.PedidoServicoStatus.CONCLUIDO,
        )
        PedidoItem.objects.create(
            pedido=pedido,
            servico=self.servico,
            recorrente=True,
            data_renovacao=None,
        )

        url = f"/api/parceria/pedidos/{pedido.id}/cancelar/"
        resp = self.auth_client.post(url)
        self.assertResponse400(resp)

        pedido.refresh_from_db()
        self.assertEqual(pedido.status_pedido_servico, PedidoServico.PedidoServicoStatus.CONCLUIDO)
        self.assertIsNone(pedido.data_fim)


    def test_cancelar_pedido_sem_itens(self):
        """Pedido sem itens deve ser cancelável"""
        pedido = PedidoServico.objects.create(
            parceria=self.parceria,
            status_pedido_servico=PedidoServico.PedidoServicoStatus.EM_ANDAMENTO,
        )

        url = f"/api/parceria/pedidos/{pedido.id}/cancelar/"
        resp = self.auth_client.post(url)

        self.assertResponse200(resp)

        pedido.refresh_from_db()
        self.assertEqual(pedido.status_pedido_servico, PedidoServico.PedidoServicoStatus.CANCELADO)
        self.assertIsNotNone(pedido.data_fim)

# ----------------------------------------------------------------------------------------
# Idempotencia
# ----------------------------------------------------------------------------------------
# Obs: concorrência real (race condition) não é coberta aqui,
# pois exige testes paralelos/threaded.


def test_criacao_pedido_idempotente_replay(self):
    """POST com mesma Idempotency-Key deve retornar replay e não criar duplicado"""
    payload = {
        "itens": [{"servico": self.servico.id}]
    }
    headers = {
        "HTTP_IDEMPOTENCY_KEY": "pedido-123"
    }

    resp1 = self.auth_client.post(
        self.view_url, payload, format="json", **headers
    )
    self.assertResponse201(resp1)

    resp2 = self.auth_client.post(
        self.view_url, payload, format="json", **headers
    )
    self.assertResponse201(resp2)

    self.assertEqual(resp1.data["id"], resp2.data["id"])
    self.assertEqual(
        PedidoServico.objects.filter(parceria=self.parceria).count(), 1
    )

def test_idempotency_key_com_payload_diferente(self):
    """Mesmo Idempotency-Key com payload diferente deve criar novo pedido"""
    headers = {
        "HTTP_IDEMPOTENCY_KEY": "pedido-456"
    }

    payload_1 = {
        "itens": [{"servico": self.servico.id}]
    }
    payload_2 = {
        "itens": [
            {"servico": self.servico.id},
            {"servico": self.servico.id},
        ]
    }

    resp1 = self.auth_client.post(
        self.view_url, payload_1, format="json", **headers
    )
    self.assertResponse201(resp1)

    resp2 = self.auth_client.post(
        self.view_url, payload_2, format="json", **headers
    )
    self.assertResponse201(resp2)

    self.assertNotEqual(resp1.data["id"], resp2.data["id"])
    self.assertEqual(
        PedidoServico.objects.filter(parceria=self.parceria).count(), 2
    )

def test_criacao_pedido_sem_idempotency_key(self):
    """POST sem Idempotency-Key deve ser rejeitado"""
    payload = {
        "itens": [{"servico": self.servico.id}]
    }

    resp = self.auth_client.post(
        self.view_url, payload, format="json"
    )

    self.assertResponse400(resp)
    self.assertEqual(
        PedidoServico.objects.filter(parceria=self.parceria).count(), 0
    )

