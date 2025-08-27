from rest_framework import status
from django.urls import reverse

from common.tests.test_utils import TestCaseUtils
from parceria.models import TicketSuporte, Parceria


class TestTicketSuporteViewSet(TestCaseUtils):
    """
    Testes de integração para endpoints de TicketSuporte.
    """

    def setUp(self):
        super().setUp()
        self.parceria = Parceria.objects.create(
            nome="Projeto Teste",
            tipo="cliente",
            proprietario=self.user,
            nome_projeto="Site Teste"
        )
        self.parceria.membros.create(user=self.user, is_active=True)
        self.list_url = reverse("parceria-tickets-list")

    def test_list_tickets_autenticado(self):
        ticket = TicketSuporte.objects.create(
            parceria=self.parceria,
            tipo="ajuda",
            titulo="Erro no painel",
            descricao="Não consigo acessar a página de pedidos.",
        )
        response = self.auth_client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(ticket.id, [item["id"] for item in response.data["results"]])

    def test_create_ticket(self):
        payload = {
            "tipo": "sugestao",
            "titulo": "Nova funcionalidade",
            "descricao": "Seria bom ter filtro de pedidos por status.",
        }
        response = self.auth_client.post(self.list_url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(TicketSuporte.objects.filter(titulo="Nova funcionalidade").exists())

    def test_retrieve_ticket(self):
        ticket = TicketSuporte.objects.create(
            parceria=self.parceria,
            tipo="problema",
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
            tipo="ajuda",
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
            tipo="outro",
            titulo="Remover conta",
            descricao="Quero apagar minha conta.",
        )
        url = reverse("parceria-tickets-detail", args=[ticket.id])
        response = self.auth_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(TicketSuporte.objects.filter(id=ticket.id).exists())

