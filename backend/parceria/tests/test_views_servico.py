from common.tests.test_utils import TestCaseUtils
from parceria.models import Servico


class TestServicoView(TestCaseUtils):
    """
    Testes de integração para o endpoint de listagem de serviços.
    """
    def setUp(self):
        """
        Cria dois serviços para validação do endpoint de listagem.
        """
        super().setUp()
        self.view_url = "/api/parceria/servicos/"
        self.servico = Servico.objects.create(
            nome="Site Zola",
            descricao="Criação de site estático",
            preco_base=500,
        )
        self.servico = Servico.objects.create(
            nome="Suporte e Manutenção",
            descricao="Manutenção de Sites estáticos",
            preco_base=50,
        )
        self.detail_url = f"/api/parceria/servicos/{self.servico.id}/"

    def test_lista_servicos_autenticado(self):
        """
        Usuário autenticado deve conseguir listar serviços com status 200 e retorno não vazio.
        """
        response = self.auth_client.get(self.view_url)
        self.assertResponse200(response)
        self.assertGreaterEqual(len(response.data['results']), 1)

    def test_lista_servicos_nao_autenticado(self):
        """Usuário não autenticado deve receber 403 ao listar serviços"""
        response = self.client.get(self.view_url)
        self.assertResponse403(response)

    def test_detalhe_servico_autenticado(self):
        """Usuário autenticado deve conseguir acessar o detalhe de um serviço"""
        response = self.auth_client.get(self.detail_url)
        self.assertResponse200(response)

    def test_detalhe_servico_nao_autenticado(self):
        """Usuário não autenticado deve receber 403 ao acessar detalhe de serviço"""
        response = self.client.get(self.detail_url)
        self.assertResponse403(response)
