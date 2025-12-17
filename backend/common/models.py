import os
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from tinymce.models import HTMLField
from model_utils.fields import AutoCreatedField, AutoLastModifiedField
from django.dispatch import receiver


class ProfessionalContactMessage(models.Model):
    """
    Modelo para armazenar mensagens enviadas atrvés do formulário de contato profissional.

    Inclui:
    - Nome e email do remetente.
    - Assunto (escolha fixa entre categorias pré-definidas).
    - Mensagem livre ( com validação anti-HTML e anti-SQL injection feita no srializer).
    - Campos UTM opcionais para rastreamento de origem.
    - Timestamp de criação.

    Segurança:
    - Os dados chegam ao banco somente após validação do reCAPTCHA e sanitização (feito no serializer).
    """

    class Meta:
        verbose_name = "Mensagem de Contato Profissional"
        verbose_name_plural = "Mensagens de Contato Profissional"

    def __str__(self):
        return f"{self.name} ({self.email}) - {self.created_at:%Y-%m-%d}"

    SUBJECT_CHOICES = [
        ("hire", "Contratação"),
        ("collab", "Parceria"),
        ("feedback", "Feedback"),
        ("question", "Dúvida"),
        ("other", "Outro"),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES)
    message = models.TextField(max_length=4000)
    utm_source = models.CharField(max_length=100, blank=True, null=True)
    utm_medium = models.CharField(max_length=100, blank=True, null=True)
    utm_campaign = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class RobotsTxt(models.Model):
    content = models.TextField(default="", help_text="Conteúdo do arquivo robots.txt")
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Arquivo robots.txt"


class IndexedTimeStampedModel(models.Model):
    created = AutoCreatedField(_("created"), db_index=True)
    modified = AutoLastModifiedField(_("modified"), db_index=True)

    class Meta:
        abstract = True


class ParametroSistema(models.Model):
    chave = models.CharField(max_length=255, unique=True, db_index=True)
    valor = models.TextField()
    ambiente = models.CharField(max_length=50)
    descricao = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.chave}  ({self.ambiente})"


class AboutMe(models.Model):
    about_image = models.ImageField(
        upload_to="about_me/",
        null=True,
        blank=True,
        validators=[
            FileExtensionValidator(allowed_extensions=["jpeg", "jpg", "png", "gif"])
        ],
    )
    about_text = HTMLField()
    social_links = models.JSONField(default=dict, blank=True)
    meta_description = models.CharField(
        max_length=160, blank=True, null=True
    )  # Meta descrição para SEO
    meta_keywords = models.CharField(
        max_length=255, blank=True, null=True
    )  # Meta palavras-chave para SEO
    last_modified = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(
        unique=True, blank=True, null=True
    )  # Slug para URL amigável

    def __str__(self):
        return "Informações sobre o dono do site"


@receiver(models.signals.post_delete, sender=AboutMe)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """Deleta arquivo do sistema quando o objeto AboutMe é removido."""
    if instance.about_image:
        instance.about_image.delete(save=False)
