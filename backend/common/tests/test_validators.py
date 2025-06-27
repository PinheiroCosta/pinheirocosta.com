from django.test import TestCase
from common.validators.sanitize import sanitize_text


class SanitizeTextValidatorTests(TestCase):

    def test_strips_html_tags(self):
        value = "<b>Olá</b>, <script>alert('xss')</script> mundo!"
        expected = (
            "Olá, alert('xss') mundo!"  # tags removidas, mas conteúdo interno mantido
        )
        result = sanitize_text(value)
        self.assertEqual(result, expected)

    def test_allows_safe_tags(self):
        value = "<b>Texto</b> com <i>ênfase</i>"
        expected = "<b>Texto</b> com <i>ênfase</i>"
        result = sanitize_text(value, tags=["b", "i"])
        self.assertEqual(result, expected)

    def test_removes_dangerous_tags_completely(self):
        value = "<script>alert('ataque')</script>Texto"
        expected = "alert('ataque')Texto"
        result = sanitize_text(value)
        self.assertEqual(result, expected)

    def test_plain_text_is_untouched(self):
        value = "Mensagem simples, sem tags."
        result = sanitize_text(value)
        self.assertEqual(result, value)
