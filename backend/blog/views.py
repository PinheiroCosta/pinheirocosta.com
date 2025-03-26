from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import BlogPost, Tag
from .serializers import BlogPostSerializer


class BlogPostPagination(PageNumberPagination):
    page_size = 6


class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.filter(status=BlogPost.PUBLICADO).order_by('-criado_em')
    serializer_class = BlogPostSerializer
    permission_classes = [AllowAny]
    pagination_class = BlogPostPagination

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

