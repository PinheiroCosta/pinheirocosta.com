import json
from io import BytesIO
from uuid import uuid4
from types import SimpleNamespace
from unittest import mock
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.db import models
from rest_framework import status
from django.contrib.admin.sites import AdminSite

from blog.services.media_upload import upload_blog_media
from blog.views import tinymce_upload
from common.tests.test_utils import TestCaseUtils
from common.storage_backends import MediaR2Storage
from common.admin import AboutMeAdmin


class TestMediaUploadService(TestCaseUtils):
    """Testes unitários e de integração para o serviço de upload de mídia do blog."""

    @mock.patch("blog.services.media_upload.default_storage")
    def test_upload_image(self, mock_storage):
        """Verifica se uma imagem é salva corretamente e retorna a URL completa."""
        file = SimpleUploadedFile("test.jpg", b"x", content_type="image/jpeg")
        mock_storage.save.return_value = "blog/images/test.jpg"
        mock_storage.url.return_value = "https://cdn.example.com/blog/images/test.jpg"

        url = upload_blog_media(file)

        self.assertEqual(url, "https://cdn.example.com/blog/images/test.jpg")
        mock_storage.save.assert_called_once_with("blog/images/test.jpg", file)

    @mock.patch("blog.services.media_upload.default_storage")
    def test_upload_video(self, mock_storage):
        """Verifica se um vídeo é salvo corretamente e retorna a URL completa."""
        file = SimpleUploadedFile("video.mp4", b"x", content_type="video/mp4")
        mock_storage.save.return_value = "blog/videos/video.mp4"
        mock_storage.url.return_value = "https://cdn.example.com/blog/videos/video.mp4"

        url = upload_blog_media(file)

        self.assertEqual(url, "https://cdn.example.com/blog/videos/video.mp4")
        mock_storage.save.assert_called_once_with("blog/videos/video.mp4", file)

    def test_upload_invalid_type(self):
        """Verifica se enviar um tipo de arquivo inválido gera ValueError."""
        file = SimpleUploadedFile("doc.pdf", b"x", content_type="application/pdf")
        with self.assertRaises(ValueError):
            upload_blog_media(file)


class TestTinyMCEUploadView(TestCaseUtils):
    """Testes para o endpoint de upload do TinyMCE usando R2."""

    def setUp(self):
        """Cria usuários staff e normal e clientes autenticados para os testes."""
        super().setUp()

        # Usuários únicos para evitar IntegrityError
        self.user_staff = self.create_user(
            email=f"staff_{uuid4()}@test.com", is_staff=True
        )
        self.user_normal = self.create_user(
            email=f"normal_{uuid4()}@test.com", is_staff=False
        )

        # Clientes autenticados
        self.auth_client_staff = self.get_authenticated_client(self.user_staff)
        self.auth_client_normal = self.get_authenticated_client(self.user_normal)

        # URL de upload do TinyMCE
        self.url = reverse("blog:tinymce-upload")

    @mock.patch("blog.views.upload_blog_media")
    def test_upload_unauthorized_user(self, mock_upload):
        """Verifica que usuários não staff não podem enviar arquivos."""
        file = SimpleUploadedFile("x.jpg", b"x")
        response = self.auth_client_normal.post(self.url, {"file": file})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("Acesso não autorizado", response.json()["error"])
        mock_upload.assert_not_called()

    @mock.patch("blog.views.upload_blog_media")
    def test_upload_no_file(self, mock_upload):
        """Verifica que enviar requisição sem arquivo retorna erro 400."""
        response = self.auth_client_staff.post(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Arquivo não enviado", response.json()["error"])
        mock_upload.assert_not_called()

    @mock.patch("blog.views.upload_blog_media")
    def test_upload_success(self, mock_upload):
        """Verifica upload bem-sucedido, retorno de URL e dados do arquivo enviados."""
        file = SimpleUploadedFile("x.jpg", b"x", content_type="image/jpeg")
        mock_upload.return_value = "https://cdn.example.com/blog/images/x.jpg"

        response = self.auth_client_staff.post(self.url, {"file": file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json()["location"], "https://cdn.example.com/blog/images/x.jpg"
        )

        # Verifica que o arquivo passado para o serviço de upload é o correto
        called_file = mock_upload.call_args[0][0]
        self.assertEqual(called_file.name, "x.jpg")
        self.assertEqual(called_file.content_type, "image/jpeg")


class TestMediaR2Storage(TestCaseUtils):
    """Testes unitários para a classe MediaR2Storage."""

    def test_get_available_name_returns_name_when_no_conflict(self):
        """Verifica que get_available_name retorna o nome original se não houver conflito."""
        storage = MediaR2Storage()
        name = "blog/images/test.jpg"
        with mock.patch.object(storage, "exists", return_value=False):
            result = storage.get_available_name(name)
            self.assertEqual(result, name)

    def test_file_overwrite_property(self):
        """Verifica que a propriedade file_overwrite está definida como False."""
        storage = MediaR2Storage()
        self.assertFalse(storage.file_overwrite)


class TestAboutMeAdminPreview(TestCaseUtils):
    """
    Testes para o método `preview` do AboutMeAdmin.
    Utiliza um modelo mínimo de teste para não depender do modelo real.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Cria um modelo de teste dinâmico com apenas o campo about_image.
        """

        class AboutMeTestModel(models.Model):
            about_image = models.ImageField(upload_to="about/", null=True, blank=True)

            class Meta:
                app_label = "common"  # necessário para registrar no admin

        cls.TestModel = AboutMeTestModel

    def setUp(self):
        """
        Inicializa o AdminSite e a instância do AboutMeAdmin.
        """
        self.site = AdminSite()
        self.admin = AboutMeAdmin(self.TestModel, self.site)

    def test_preview_no_image(self):
        """
        Verifica que o preview retorna '(Sem Imagem)' quando about_image é None.
        """
        obj = self.TestModel()
        obj.about_image = None
        self.assertEqual(self.admin.preview(obj), "(Sem Imagem)")

    def test_preview_with_image_url(self):
        """
        Verifica que o preview retorna uma tag <img> com a URL correta quando existe about_image.
        """

        class FakeImage:
            url = "https://cdn.example.com/test.jpg"

        obj = self.TestModel()
        obj.about_image = FakeImage()
        result = self.admin.preview(obj)
        self.assertIn("img", result)
        self.assertIn("https://cdn.example.com/test.jpg", result)
