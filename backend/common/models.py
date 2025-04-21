from django.core.files.uploadedfile import UploadedFile
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from tinymce.models import HTMLField
from model_utils.fields import AutoCreatedField, AutoLastModifiedField
import base64
from PIL import Image
import io


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

    def process_temp_image(self):
        if not self.temp_image:
            return
        
        try:
            if hasattr(self.temp_image, 'seek') and hasattr(self.temp_image, 'read'):
                self.temp_image.seek(0) # Garante que está no inicio da leitura
                img = Image.open(self.temp_image)
                img_format = img.format.lower()

                if img_format not in ["jpg", "jpeg", "png", "gif"]:
                    raise ValidationError(f"Formato inválido: {img_format}. Use JPG, JPEG, PNG, ou GIF.")

                buffered = io.BytesIO()
                img.save(buffered, format=img_format.upper())
                encoded_string = base64.b64encode(buffered.getvalue()).decode("utf-8")
                self.about_image = f"data:image/{img_format};base64,{encoded_string}"
            else:
                raise ValidationError("Imagem inválida ou ausente.")

            self.temp_image = None
        except Exception as e:
            raise ValidationError(f"Erro ao processar a imagem: {str(e)}")

    def save(self, *args, **kwargs):
        if not self.pk and AboutMe.objects.exists():
            raise ValidationError("Só pode existir um único registro de 'Sobre Mim'.")

        self.process_temp_image()
        super().save(*args, **kwargs)

    def __str__(self):
        return "Informações sobre o dono do site"
