from django.views.generic import DetailView
from django.http import Http404
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from .models import BlogPost, Tag
from .serializers import BlogPostSerializer


class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = "blog/post_detail.html"

    def get_object(self, queryset=None):
        slug = self.kwargs.get("slug")
        try:
            return BlogPost.objects.get(slug=slug, status=BlogPost.PUBLICADO)
        except BlogPost.DoesNotExist:
            raise Http404("Post não encontrado")


class BlogPostPagination(PageNumberPagination):
    page_size = 6


class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.filter(status=BlogPost.PUBLICADO).order_by('-criado_em')
    serializer_class = BlogPostSerializer
    permission_classes = [AllowAny]
    pagination_class = BlogPostPagination

    def get_queryset(self):
        """Aplica filtros dinâmicos."""
        queryset = self.queryset
        tag = self.request.query_params.get('tag')

        if tag:
            queryset = queryset.filter(tags__nome=tag)

        return queryset

        
    @action(detail=False, methods=['get'], url_path='tag/(?P<tag>[^/.]+)')
    def by_tag(self, request, tag=None):
        posts = BlogPost.objects.filter(tags__nome=tag, status=BlogPost.PUBLICADO)
        serializer = BlogPostSerializer(posts, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='slug/(?P<slug>[^/.]+)')
    def by_slug(self, request, slug=None):
        try:
            post = BlogPost.objects.get(slug=slug, status=BlogPost.PUBLICADO)
            serializer = BlogPostSerializer(post)
            return Response(serializer.data)
        except BlogPost.DoesNotExist:
            raise NotFound(detail="Post não encontrado com esse slug.")

