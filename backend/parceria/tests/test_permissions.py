from common.tests.test_utils import TestCaseUtils
from model_bakery import baker
from parceria.models import Servico


class TestParceriaPermissions(TestCaseUtils):
    """
    Verifica regras de acesso e proteção de dados da API de parceria.
    """
    def setUp(self):
        """
        Prepara um usuário não autenticado e um objeto pertencente a outro usuário.
        """
        super().setUp()
        self.outro_user = baker.make("users.User")
        self.servico = baker.make(Servico)
        self.url = f"/api/parceria/servicos/{self.servico.id}/"

    def test_usuario_nao_autenticado_recebe_403(self):
        """
        Usuário não autenticado deve receber 403 ao tentar acessar detalhes de um serviço.
        """
        client = self.client  
        response = client.get(self.url)
        self.assertResponse403(response)
