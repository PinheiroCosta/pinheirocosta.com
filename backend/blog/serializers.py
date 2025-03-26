from rest_framework import serializers
from .models import BlogPost, Tag
from django.contrib.auth.models import User


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'nome']

class BlogPostSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)  # Serializa as tags associadas
    nome_autor = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = ['id', 'slug', 'nome_autor', 'titulo', 'conteudo', 'criado_em', 'atualizado_em', 'tags']


    def get_nome_autor(self, obj):
        autor = obj.autor
        if autor and autor.email:
            nome = autor.email.split('@')[0]        
            return ' '.join(word.capitalize() for word in nome.split('.'))
        return "Autor Desconhecido"
