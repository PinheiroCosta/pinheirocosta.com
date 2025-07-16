from django.test import TestCase
from django.urls import reverse

from model_bakery import baker
from rest_framework.test import APIClient


class TestCaseUtils(TestCase):
    """
    Classe base utilitária para testes com usuários autenticados.
    Fornece cliente autenticado, reverso de URLs e asserções comuns de status HTTP.
    """
    def setUp(self):
        self._user_password = "123456"

        self.user = baker.prepare("users.User", email="user@email.com")
        self.user.set_password(self._user_password)
        self.user.save()
        self.auth_client = APIClient()
        self.auth_client.login(email=self.user.email, password=self._user_password)

        self.user_b = baker.prepare("users.User", email="user_b@email.com")
        self.user_b.set_password(self._user_password)
        self.user_b.save()
        self.auth_client_b = APIClient()
        self.auth_client_b.login(email=self.user.email, password=self._user_password)


    def reverse(self, name, *args, **kwargs):
        """Reverse a url, convenience to avoid having to import reverse in tests"""
        return reverse(name, args=args, kwargs=kwargs)

    def assertResponse200(self, response):
        """Given response has status_code 200 OK"""
        self.assertEqual(response.status_code, 200)

    def assertResponse201(self, response):
        """Given response has status_code 201 CREATED"""
        self.assertEqual(response.status_code, 201)

    def assertResponse204(self, response):
        """Given response has status_code 204 NO CONTENT"""
        self.assertEqual(response.status_code, 204)

    def assertResponse301(self, response):
        """Given response has status_code 301 MOVED PERMANENTLY"""
        self.assertEqual(response.status_code, 301)

    def assertResponse302(self, response):
        """Given response has status_code 302 FOUND"""
        self.assertEqual(response.status_code, 302)

    def assertResponse400(self, response):
        """Given response has status_code 400 BAD REQUEST"""
        self.assertEqual(response.status_code, 400)

    def assertResponse401(self, response):
        """Given response has status_code 401 UNAUTHORIZED"""
        self.assertEqual(response.status_code, 401)

    def assertResponse403(self, response):
        """Given response has status_code 403 FORBIDDEN"""
        self.assertEqual(response.status_code, 403)

    def assertResponse404(self, response):
        """Given response has status_code 404 NOT FOUND"""
        self.assertEqual(response.status_code, 404)


class TestGetRequiresAuthenticatedUser:
    """
    Testa se o acesso GET requer autenticação.
    Deve ser herdado por outras classes de teste que definem `view_url`.
    """
    def test_get_requires_authenticated_user(self):
        response = self.client.get(self.view_url)
        self.assertResponse403(response)


class TestAuthGetRequestSuccess:
    """
    Testa se o acesso autenticado à `view_url` retorna 200 OK.
    Deve ser herdado por outras classes de teste.
    """
    def test_auth_get_success(self):
        response = self.auth_client.get(self.view_url)
        self.assertResponse200(response)
