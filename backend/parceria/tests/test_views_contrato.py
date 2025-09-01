from django.utils import timezone
from django.urls import reverse
from parceria.models import Parceria, ParceriaMembro, ContratoServico, Servico
from common.tests.test_utils import TestCaseUtils


class TestContratoServicoView(TestCaseUtils):

    def setUp(self):
        super().setUp()

        self.parceria1 = Parceria.objects.create(
            nome="Cliente 1",
            tipo_parceria="cliente",
            nome_projeto="projeto1",
            dominio="p1.com",
            proprietario=self.user
        )
        ParceriaMembro.objects.create(parceria=self.parceria1, user=self.user, is_active=True)

        self.parceria2 = Parceria.objects.create(
            nome="Cliente 2",
            tipo_parceria="cliente",
            nome_projeto="projeto2",
            dominio="p2.com",
            proprietario=self.user_b
        )
        ParceriaMembro.objects.create(parceria=self.parceria2, user=self.user_b, is_active=True)

        # Serviço e contratos
        self.servico = Servico.objects.create(
            nome="Serviço Teste",
            descricao="desc",
            preco=100,
            periodicidade_servico="mensal"
        )
        self.contrato1 = ContratoServico.objects.create(parceria=self.parceria1, servico=self.servico)
        self.contrato2 = ContratoServico.objects.create(parceria=self.parceria2, servico=self.servico)

        # URLs
        self.list_url = reverse("parceria-contratos-list")
        self.detail_url_1 = reverse("parceria-contratos-detail", args=[self.contrato1.id])
        self.detail_url_2 = reverse("parceria-contratos-detail", args=[self.contrato2.id])

    def test_list_retorna_somente_contratos_do_usuario(self):
        response = self.auth_client.get(self.list_url)
        self.assertResponse200(response)
        ids = [c["id"] for c in response.data["results"]]
        self.assertIn(self.contrato1.id, ids)
        self.assertNotIn(self.contrato2.id, ids)

    def test_detail_de_outro_usuario_retorna_404(self):
        response = self.auth_client.get(self.detail_url_2)
        self.assertResponse404(response)

    def test_update_de_outro_usuario_retorna_404(self):
        payload = {"observacoes": "tentativa de alteração"}
        response = self.auth_client.patch(self.detail_url_2, payload, format="json")
        self.assertResponse404(response)

    def test_delete_de_outro_usuario_retorna_403(self):
        response = self.auth_client.delete(self.detail_url_2)
        self.assertResponse403(response)

    def test_criacao_associa_parceria_do_usuario_ignorando_payload(self):
        payload = {
            "servico": self.servico.id,
            "parceria": self.parceria2.id,  # tentativa de criar para outra parceria
            "data_inicio": timezone.now().isoformat(),
            "observacoes": "Teste criação",
        }
        response = self.auth_client.post(self.list_url, payload, format="json")
        self.assertResponse201(response)

        contrato_id = response.data["id"]
        contrato = ContratoServico.objects.get(id=contrato_id)
        self.assertEqual(contrato.parceria, self.parceria1)

    def test_usuario_nao_autenticado_nao_pode_acessar(self):
        client = self.client
        urls = [self.list_url, self.detail_url_1]
        for url in urls:
            response = client.get(url)
            self.assertIn(response.status_code, (403, 401))

