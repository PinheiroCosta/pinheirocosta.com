from common.tests.test_utils import TestCaseUtils
from django.core.cache import cache
from django.test import Client
import itertools


ip_generator = itertools.count(1)


class TestProfessionalContactMessage(TestCaseUtils):
    def setUp(self):
        super().setUp()
        self.url = "/api/contato-profissional/"
        ip_suffix = next(ip_generator)
        test_ip = f"192.0.2.{ip_suffix}"
        self.client = Client(REMOTE_ADDR=test_ip)

    def tearDown(self):
        cache.clear()

    def test_valid_post_returns_201(self):
        payload = {
            "name": "João da Silva",
            "email": "joao@email.com",
            "subject": "hire",
            "message": "Gostaria de contratar seus serviços.",
        }
        response = self.client.post(self.url, data=payload, format="json")
        self.assertResponse201(response)

    def test_missing_required_field_returns_400(self):
        payload = {
            "email": "joao@email.com",
            "subject": "hire",
            "message": "Faltando o nome.",
        }
        response = self.client.post(self.url, data=payload, format="json")
        self.assertResponse400(response)
        self.assertIn("name", response.json())

    def test_invalid_email_returns_400(self):
        payload = {
            "name": "João",
            "email": "email-invalido",
            "subject": "hire",
            "message": "Mensagem qualquer",
        }
        response = self.client.post(self.url, data=payload, format="json")
        self.assertResponse400(response)
        self.assertIn("email", response.json())

    def test_invalid_subject_returns_400(self):
        payload = {
            "name": "João",
            "email": "joao@email.com",
            "subject": "invalid-subject",
            "message": "Mensagem qualquer",
        }
        response = self.client.post(self.url, data=payload, format="json")
        self.assertResponse400(response)
        self.assertIn("subject", response.json())

    def test_unauthenticated_post_is_allowed(self):
        payload = {
            "name": "Anônimo",
            "email": "anon@email.com",
            "subject": "other",
            "message": "Mensagem pública",
        }
        response = self.client.post(self.url, data=payload, format="json")
        self.assertResponse201(response)

    def test_name_too_long_returns_400(self):
        payload = {
            "name": "A" * 300,
            "email": "joao@email.com",
            "subject": "hire",
            "message": "Mensagem qualquer",
        }
        response = self.client.post(self.url, data=payload, format="json")
        self.assertResponse400(response)
        self.assertIn("name", response.json())


class TestProfessionalContactMessageSecurity(TestCaseUtils):
    def setUp(self):
        super().setUp()
        self.url = "/api/contato-profissional/"
        ip_suffix = next(ip_generator)
        test_ip = f"192.0.2.{ip_suffix}"
        self.client = Client(REMOTE_ADDR=test_ip)

    def tearDown(self):
        cache.clear()

    def test_xss_injection_in_message(self):
        payload = {
            "name": "Hacker",
            "email": "hacker@example.com",
            "subject": "hire",
            "message": "<script>alert('XSS')</script>",
        }
        response = self.client.post(self.url, data=payload, format="json")
        self.assertResponse400(response)  # ou ajustar conforme sua regra de negócio

    def test_html_tags_in_name(self):
        payload = {
            "name": "<img src=x onerror=alert(1)>",
            "email": "user@example.com",
            "subject": "hire",
            "message": "Teste HTML tags no nome",
        }
        response = self.client.post(self.url, data=payload, format="json")
        self.assertResponse400(response)

    def test_sql_injection_in_message(self):
        payload = {
            "name": "SQLi",
            "email": "sqli@example.com",
            "subject": "hire",
            "message": "admin'; DROP TABLE users; --",
        }
        response = self.client.post(self.url, data=payload, format="json")
        self.assertResponse400(response)

    def test_sql_injection_in_name(self):
        payload = {
            "name": "' OR 1=1 --",
            "email": "sqli2@example.com",
            "subject": "hire",
            "message": "Tentando SQL Injection no nome",
        }
        response = self.client.post(self.url, data=payload, format="json")
        self.assertResponse400(response)

    def test_rate_limit_blocks_after_ten_requests(self):
        payload = {
            "name": "Teste Rate Limit",
            "email": "ratelimit@example.com",
            "subject": "hire",
            "message": "Testando limite de envio",
        }

        for _ in range(10):
            response = self.client.post(self.url, data=payload, format="json")
            self.assertResponse201(response)

        # Quarta tentativa deve ser bloqueada
        response = self.client.post(self.url, data=payload, format="json")
        self.assertEqual(response.status_code, 429)
