import os
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from tinymce.models import HTMLField
from model_utils.fields import AutoCreatedField, AutoLastModifiedField
from django.dispatch import receiver


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
        return f'{self.chave}  ({self.ambiente})'


class AboutMe(models.Model):
    about_image = models.ImageField(
        upload_to="about_me/",
        null=True, 
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpeg', 'jpg', 'png', 'gif'])]
    )
    about_text = HTMLField()  
    social_links = models.JSONField(default=dict, blank=True)
    meta_description = models.CharField(max_length=160, blank=True, null=True)  # Meta descrição para SEO
    meta_keywords = models.CharField(max_length=255, blank=True, null=True)  # Meta palavras-chave para SEO
    last_modified = models.DateTimeField(auto_now=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True, null=True)  # Slug para URL amigável

    def save(self, *args, **kwargs):
        try:
            old = AboutMe.objects.get(id=self.id)
            if old.about_image and old.about_image != self.about_image:
                if os.path.isfile(old.about_image.path):
                    os.remove(old.about_image.path)
        except AboutMe.DoesNotExist:
            pass
        super().save(*args, **kwargs)

    def __str__(self):
        return "Informações sobre o dono do site"


@receiver(models.signals.post_delete, sender=AboutMe)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """Deleta arquivo do sistema quando o objeto AboutMe é removido."""
    if instance.about_image and os.path.isfile(instance.about_image.path):
        os.remove(instance.about_image.path)
