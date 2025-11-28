from django.utils import timezone
from django.urls import reverse
from parceria.models import Parceria, ParceriaMembro, ContratoServico, Servico
from common.tests.test_utils import TestCaseUtils


class TestContratoServicoView(TestCaseUtils):

    def setUp(self):
        super().setUp()

        self.parceria1 = Parceria.objects.create(
            nome="Cliente 1",
            natureza="pf",
            categoria="cliente",
            dominio="p1.com",
            proprietario=self.user
        )
        ParceriaMembro.objects.create(parceria=self.parceria1, usuario=self.user, ativo=True)

        self.parceria2 = Parceria.objects.create(
            nome="Cliente 2",
            natureza="pf",
            categoria="cliente",
            dominio="p2.com",
            proprietario=self.user_b
        )
        ParceriaMembro.objects.create(parceria=self.parceria2, usuario=self.user_b, ativo=True)

        # Serviço e contratos
        self.servico = Servico.objects.create(
            nome="Serviço Teste",
            descricao="desc",
            preco_base=100,
        )
        self.contrato1 = ContratoServico.objects.create(parceria=self.parceria1, observacoes="Criado pela suite de testes")
        self.contrato2 = ContratoServico.objects.create(parceria=self.parceria2, observacoes="Criado pela suite de testes")

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

