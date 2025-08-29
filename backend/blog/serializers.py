from rest_framework import serializers
from django.contrib.auth.models import User
from drf_spectacular.utils import extend_schema_field
from .models import BlogPost, Tag


class TagSerializer(serializers.ModelSerializer):
    """Serializador para o modelo Tag."""

    class Meta:
        model = Tag
        fields = ["id", "nome"]


class BlogPostSerializer(serializers.ModelSerializer):
    """
    Serializador para o modelo BlogPost. Inclui nome formatado do autor (extraído do email) e lista de tags.
    """

    tags = TagSerializer(many=True)  # Serializa as tags associadas
    nome_autor = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = [
            "id",
            "slug",
            "nome_autor",
            "titulo",
            "conteudo",
            "criado_em",
            "atualizado_em",
            "tags",
        ]

    @extend_schema_field(serializers.CharField())
    def get_nome_autor(self, obj) -> str:
        """
        Retorna o nome do autor baseado na parte local do email.
        Se o autor não possuir email, retorna 'Autor Desconhecido'.
        """

        autor = obj.autor
        if autor and autor.email:
            nome = autor.email.split("@")[0]
            return " ".join(word.capitalize() for word in nome.split("."))
        return "Autor Desconhecido"
