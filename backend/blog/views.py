from django.views.generic import TemplateView
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from .models import BlogPost
from .serializers import BlogPostSerializer
from .services.media_upload import upload_blog_media



class BlogPostDetailView(TemplateView):
    """Serve o template base para o frontend (SPA)."""

    template_name = "common/index.html"


class BlogPostViewSet(viewsets.ModelViewSet):
    """
    API para listagem, filtro e recuperação de posts do blog.
    """

    queryset = BlogPost.objects.filter(status=BlogPost.PUBLICADO).order_by("-criado_em")
    serializer_class = BlogPostSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["tags__nome"]
    lookup_field = "slug"


@csrf_exempt
@require_POST
def tinymce_upload(request):
    if not request.user.is_staff:
        return JsonResponse({"error": "Acesso não autorizado."}, status=403)

    file = request.FILES.get("file")
    if not file:
        return JsonResponse({"error": "Arquivo não enviado"}, status=400)

    try:
        url = upload_blog_media(file)
    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"location": url})

