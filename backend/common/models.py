import imghdr
import base64
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from tinymce.models import HTMLField
from model_utils.fields import AutoCreatedField, AutoLastModifiedField


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
    about_image = models.TextField(null=True, blank=True)
    about_text = HTMLField()  
    social_links = models.JSONField(default=dict, blank=True)
    meta_description = models.CharField(max_length=160, blank=True, null=True)  # Meta descrição para SEO
    meta_keywords = models.CharField(max_length=255, blank=True, null=True)  # Meta palavras-chave para SEO
    last_modified = models.DateTimeField(auto_now=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True, null=True)  # Slug para URL amigável
    temp_image = models.ImageField(
        upload_to="temp_uploads/", null=True, blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])]
    )

    def save(self, *args, **kwargs):
        if not self.pk and AboutMe.objects.exists():
            raise ValidationError("Só pode existir um único registro de 'Sobre Mim'.")
        if self.temp_image:
            self.temp_image.save(self.temp_image.name, self.temp_image, save=False)
            try:
                file_format = imghdr.what(self.temp_image.path)
                if file_format not in ["jpg", "jpeg", "png", "gif"]:
                    raise ValueError("Formato de imagem inválido. Use JPG, JPEG, PNG, ou GIF.")

                with self.temp_image.open("rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
                    self.about_image = f"data:image/{file_format};base64,{encoded_string}"

                self.temp_image.delete(save=False)
            except Exception as e:
                raise ValidationError(f"Erro ao processar a imagem: {str(e)}")

        super().save(*args, **kwargs)

    def __str__(self):
        return "Informações sobre o dono do site"
