from django.db import models
from django.conf import settings
from tinymce.models import HTMLField
from django.utils.text import slugify
from django.urls import reverse


class Tag(models.Model):
    nome = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nome

class BlogPost(models.Model):
    RASCUNHO = 'rascunho'
    PUBLICADO = 'publicado'
    ARQUIVADO = 'arquivado'
    ARTICLE_STATUS = [
        ("rascunho", "Rascunho"),
        ("publicado", "Publicado"),
        ("arquivado", "Arquivado"),
    ]

    titulo = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True, null=True)
    conteudo = HTMLField()  # TinyMCE será usado aqui
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, related_name="posts")
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts")
    status = models.CharField(max_length=10, choices=ARTICLE_STATUS, default="rascunho")

    class Meta:
        ordering = ["-criado_em"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse("blog:post_detail", kwargs={"slug": self.slug})
