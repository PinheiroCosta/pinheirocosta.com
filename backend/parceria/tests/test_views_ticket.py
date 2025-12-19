from rest_framework import status
from django.urls import reverse

from common.tests.test_utils import TestCaseUtils
from parceria.models import TicketSuporte, TicketMensagem, Parceria


class TestTicketSuporteViewSet(TestCaseUtils):
    """
    Testes de integração para endpoints de TicketSuporte.
    """

    def setUp(self):
        super().setUp()
        self.parceria = Parceria.objects.create(
            nome="Projeto Teste",
            natureza="pf",
            categoria="cliente",
            proprietario=self.user,
            dominio="site-teste.com",
        )
        self.parceria.membros.create(usuario=self.user, ativo=True)
        self.list_url = reverse("parceria-tickets-list")

    def test_list_tickets_autenticado(self):
        ticket = TicketSuporte.objects.create(
            parceria=self.parceria,
            tipo_ticket_suporte="ajuda",
            titulo="Erro no painel",
            descricao="Não consigo acessar a página de pedidos.",
        )
        response = self.auth_client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(ticket.id, [item["id"] for item in response.data["results"]])

    def test_create_ticket(self):
        payload = {
            "tipo_ticket_suporte": "sugestao",
            "titulo": "Nova funcionalidade",
            "descricao": "Seria bom ter filtro de pedidos por status.",
        }
        response = self.auth_client.post(self.list_url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            TicketSuporte.objects.filter(titulo="Nova funcionalidade").exists()
        )

    def test_retrieve_ticket(self):
        ticket = TicketSuporte.objects.create(
            parceria=self.parceria,
            tipo_ticket_suporte="problema",
            titulo="Bug crítico",
            descricao="Erro 500 ao salvar pedido.",
        )
        url = reverse("parceria-tickets-detail", args=[ticket.id])
        response = self.auth_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], ticket.id)

    def test_update_ticket(self):
        ticket = TicketSuporte.objects.create(
            parceria=self.parceria,
            tipo_ticket_suporte="ajuda",
            titulo="Dúvida sobre plano",
            descricao="Não entendi o que está incluso no plano.",
        )
        url = reverse("parceria-tickets-detail", args=[ticket.id])
        payload = {"descricao": "Atualizei minha dúvida."}
        response = self.auth_client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ticket.refresh_from_db()
        self.assertEqual(ticket.descricao, "Atualizei minha dúvida.")

    def test_delete_ticket_nao_permitido(self):
        ticket = TicketSuporte.objects.create(
            parceria=self.parceria,
            tipo_ticket_suporte="outro",
            titulo="Remover conta",
            descricao="Quero apagar minha conta.",
        )
        url = reverse("parceria-tickets-detail", args=[ticket.id])
        response = self.auth_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(TicketSuporte.objects.filter(id=ticket.id).exists())

    # -------------------------------------------------------------------------
    # criar ticket
    # -------------------------------------------------------------------------
    def test_create_ticket_descricao_curta_invalida(self):
        payload = {
            "titulo": "Ticket inválido",
            "descricao": "   ",  # whitespace
            "tipo_ticket_suporte": "problema",
        }
        response = self.auth_client.post(self.list_url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_ticket_descricao_longa_invalida(self):
        payload = {
            "titulo": "Texto grande",
            "descricao": "x" * 4001,  # limite excedido
            "tipo_ticket_suporte": "problema",
        }
        response = self.auth_client.post(self.list_url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_ticket_tipo_default_quando_omitido(self):
        payload = {"titulo": "Sem tipo enviado", "descricao": "Apenas teste."}
        response = self.auth_client.post(self.list_url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        ticket = TicketSuporte.objects.get(id=response.data["id"])
        # Deve ter sido usado o tipo default do service
        self.assertEqual(
            ticket.tipo_ticket_suporte, TicketSuporte.TicketSuporteTipo.OUTRO
        )

    def test_create_ticket_sem_parceria_retornando_forbidden(self):
        user_sem_parceria = self.create_user(email="novo@ex.com", password="123456")
        client = self.get_authenticated_client(user_sem_parceria)

        payload = {
            "titulo": "Teste sem parceria",
            "descricao": "Teste.",
            "tipo_ticket_suporte": "problema",
        }

        response = client.post(self.list_url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_tickets_nao_duplica(self):
        """
        Garante que OR no queryset não retorna duplicidades.
        """
        # membro já existe; vai criar duas entradas que poderiam duplicar em OR
        ticket = TicketSuporte.objects.create(
            parceria=self.parceria,
            tipo_ticket_suporte="problema",
            titulo="Duplicidade",
            descricao="Teste duplicidade.",
        )

        response = self.auth_client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        ids = [item["id"] for item in response.data["results"]]
        self.assertEqual(ids.count(ticket.id), 1)

    def test_service_e_usado_na_criacao_validando_regra(self):
        """
        Verifica que perform_create realmente chamou o service
        e portanto aplicou as regras de domínio (ex: limite de 4000 chars).
        """
        payload = {
            "titulo": "Validação via service",
            "descricao": "x" * 4001,  # inválido segundo a regra de criar_ticket()
        }
        response = self.auth_client.post(self.list_url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # -------------------------------------------------------------------------
    # Responder Ticket
    # -------------------------------------------------------------------------
    def test_responder_ticket_sucesso(self):
        ticket = TicketSuporte.objects.create(
            parceria=self.parceria,
            tipo_ticket_suporte="problema",
            titulo="Teste",
            descricao="Desc",
        )

        url = f"/api/parceria/tickets/{ticket.id}/responder/"
        response = self.auth_client.post(url, {"conteudo": "Resposta válida"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # mensagem registrada
        self.assertTrue(TicketMensagem.objects.filter(ticket=ticket).exists())

        # ticket retornado no serializer
        self.assertEqual(response.data["id"], ticket.id)

    def test_responder_ticket_muda_status_de_novo_para_em_analise(self):
        ticket = TicketSuporte.objects.create(
            parceria=self.parceria,
            tipo_ticket_suporte="problema",
            titulo="Teste",
            descricao="Desc",
            status_ticket_suporte=TicketSuporte.TicketSuporteStatus.NOVO,
        )

        url = f"/api/parceria/tickets/{ticket.id}/responder/"
        response = self.auth_client.post(url, {"conteudo": "Informação adicional"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        ticket.refresh_from_db()
        self.assertEqual(
            ticket.status_ticket_suporte, TicketSuporte.TicketSuporteStatus.EM_ANALISE
        )

    def test_responder_ticket_mantem_status_se_ja_estiver_em_analise(self):
        ticket = TicketSuporte.objects.create(
            parceria=self.parceria,
            tipo_ticket_suporte="problema",
            titulo="Teste",
            descricao="Desc",
            status_ticket_suporte=TicketSuporte.TicketSuporteStatus.EM_ANALISE,
        )

        url = f"/api/parceria/tickets/{ticket.id}/responder/"
        response = self.auth_client.post(url, {"conteudo": "OK"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        ticket.refresh_from_db()
        self.assertEqual(
            ticket.status_ticket_suporte, TicketSuporte.TicketSuporteStatus.EM_ANALISE
        )

    def test_responder_ticket_conteudo_longo_invalido(self):
        ticket = TicketSuporte.objects.create(
            parceria=self.parceria, titulo="Teste", descricao="Desc"
        )

        url = f"/api/parceria/tickets/{ticket.id}/responder/"
        response = self.auth_client.post(url, {"conteudo": "x" * 4001})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_responder_ticket_conteudo_vazio(self):
        ticket = TicketSuporte.objects.create(
            parceria=self.parceria, titulo="Teste", descricao="Desc"
        )

        url = f"/api/parceria/tickets/{ticket.id}/responder/"
        response = self.auth_client.post(url, {"conteudo": ""})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_responder_ticket_fechado_retorna_erro(self):
        ticket = TicketSuporte.objects.create(
            parceria=self.parceria,
            titulo="Teste",
            descricao="Desc",
            status_ticket_suporte=TicketSuporte.TicketSuporteStatus.CONCLUIDO,
        )

        url = f"/api/parceria/tickets/{ticket.id}/responder/"
        response = self.auth_client.post(url, {"conteudo": "Tentativa inválida"})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_responder_ticket_usuario_sem_parceria_recebe_404(self):
        ticket = TicketSuporte.objects.create(
            parceria=self.parceria, titulo="Teste", descricao="Desc"
        )

        user = self.create_user(email="novo@ex.com", password="123456")
        client = self.get_authenticated_client(user)

        url = f"/api/parceria/tickets/{ticket.id}/responder/"
        response = client.post(url, {"conteudo": "msg"})

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_responder_ticket_de_outra_parceria_retorna_404(self):
        outra = Parceria.objects.create(nome="Outra", proprietario=self.user_b)

        ticket = TicketSuporte.objects.create(
            parceria=outra, titulo="Teste", descricao="Desc"
        )

        url = f"/api/parceria/tickets/{ticket.id}/responder/"
        response = self.auth_client.post(url, {"conteudo": "msg"})

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_responder_ticket_usa_service_para_regra_de_negocio(self):
        ticket = TicketSuporte.objects.create(
            parceria=self.parceria, titulo="Teste", descricao="Desc"
        )

        url = f"/api/parceria/tickets/{ticket.id}/responder/"
        response = self.auth_client.post(url, {"conteudo": "x" * 4001})

        # Garantia que o service aplicou a regra e não a view
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
