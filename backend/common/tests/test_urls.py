from django.test import TestCase
from django.urls import reverse
from django.conf import settings


class PublicURLsTests(TestCase):
    """Testes básicos para URLs públicas e endpoints de dev."""

    def test_homepage_common(self):
        """Verifica se a homepage (common) retorna 200"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_robots_txt(self):
        """Verifica se /robots.txt retorna 200 e contém User-agent"""
        response = self.client.get("/robots.txt")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"User-Agent", response.content)

    def test_sitemap_xml(self):
        """Verifica se /sitemap.xml retorna 200 e contém <urlset>"""
        response = self.client.get("/sitemap.xml")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"<urlset", response.content)

    def test_swagger_redoc_schema(self):
        """Verifica endpoints do drf-spectacular"""
        for url in ["/api/schema/", "/api/schema/swagger-ui/", "/api/schema/redoc/"]:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)

    def test_api_router_root(self):
        """Verifica se /api/ responde com 403 se acesso nao autenticado"""
        response = self.client.get("/api/")
        self.assertEqual(response.status_code, 403)

    def test_media_serving_dev(self):
        """Testa se URLs de media funcionam (somente em dev)"""
        if settings.DEBUG:
            response = self.client.get(f"{settings.MEDIA_URL}placeholder.txt")
            # Só checa se não retorna 500, 404 é aceitável se arquivo não existir
            self.assertNotEqual(response.status_code, 500)

    def test_optional_urls_import(self):
        """Smoke test: importa todos OPTIONAL_APPS sem incluir no urlpatterns"""
        from importlib import import_module
        OPTIONAL_APPS = {
            "blog": "blog.urls_registry",
            "tools": "tools.urls_registry",
            "motd": "motd.urls_registry",
            "parceria": "parceria.urls_registry",
        }
        for app, module_path in OPTIONAL_APPS.items():
            if getattr(settings, "OPTIONAL_APPS", {}).get(app, False):
                with self.subTest(app=app):
                    mod = import_module(module_path)
                    self.assertTrue(hasattr(mod, "URLPATTERNS") or hasattr(mod, "ROUTES"))
