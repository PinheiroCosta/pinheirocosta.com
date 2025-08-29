from django.test import TestCase
from django.urls import reverse


class CommonViewsTests(TestCase):
    def test_robots_txt(self):
        """Verifica se /robots.txt retorna 200 e contém 'User-agent'"""
        response = self.client.get("/robots.txt")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"User-Agent", response.content)

    def test_sitemap_xml(self):
        """Verifica se /sitemap.xml retorna 200 e contém a tag <urlset>"""
        response = self.client.get("/sitemap.xml")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"<urlset", response.content)
