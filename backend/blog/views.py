from django.views.generic import TemplateView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from .models import BlogPost
from .serializers import BlogPostSerializer


class BlogPostDetailView(TemplateView):
    """Serve o template base para o frontend (SPA)."""

    template_name = "common/index.html"


class BlogPostViewSet(viewsets.ModelViewSet):
    """
    API para listagem, filtro e recuperação de posts do blog.
    """

    queryset = BlogPost.objects.filter(status=BlogPost.PUBLICADO).order_by('-criado_em')
    serializer_class = BlogPostSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tags__nome']
    lookup_field = 'slug'
