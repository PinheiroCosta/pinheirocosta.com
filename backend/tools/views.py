import random
import requests
from django.views.generic import TemplateView
from django.http import JsonResponse
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema
from drf_spectacular.types import OpenApiTypes
from .models import Tool
from .serializers import ToolSerializer


TIMEOUT_SECONDS = 5
MAX_RETRIES = 3

class ToolDetailView(TemplateView):
    template_name = "common/index.html"

    
class ToolViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Tool.objects.filter(active=True)
    serializer_class = ToolSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'category'] 
    lookup_field = 'slug'

    @method_decorator(ratelimit(key='ip', rate='30/m', method='POST', block=True))
    @method_decorator(ratelimit(key='ip', rate='60/m', method='POST', group='global', block=True))
    @extend_schema(operation_id="proxyTool", request=OpenApiTypes.OBJECT, responses=OpenApiTypes.OBJECT)
    @action(detail=False, methods=["post"], url_path="proxy/(?P<slug>[^/.]+)")
    def proxy_tool(self, request, slug):
        """Encaminha a requisição para a API da ferramenta usando slug"""

        try: # Valida existencia da ferramenta no banco
            tool = Tool.objects.get(slug=slug, active=True)
        except Tool.DoesNotExist:
            return JsonResponse({"error": f"Tool '{slug}' not found"}, status=404)

        for attempt in range(MAX_RETRIES):
            try:
                response = requests.post(
                    tool.api_url,
                    json=request.data,
                    headers={"Content-Type": "application/json"},
                    timeout=TIMEOUT_SECONDS
                )
                return JsonResponse(response.json(), status=response.status_code)
            except requests.Timeout:
                if attempt == MAX_RETRIES - 1:
                    return JsonResponse({"error": "Request timeout"}, status=504)
            except requests.RequestException as e:
                if attempt == MAX_RETRIES - 1:
                    return JsonResponse({"error": "Service unavailable"}, status=503)
        
    @action(detail=False, methods=['get'], url_path='slug/(?P<slug>[^/.]+)')
    def by_slug(self, request, slug=None):
        try:
            tool = Tool.objects.get(slug=slug, active=True)
            serializer = ToolSerializer(tool)
            return Response(serializer.data)
        except Tool.DoesNotExist:
            return Response({'detail': 'Ferramenta não encontrada'}, status=status.HTTP_NOT_FOUND)

    @action(detail=False, methods=["get"], url_path="random")
    def random_tool(self, request):
        count = self.queryset.count()
        if count == 0:
            return Response({"detail": "Nenhuma ferramenta disponível."}, status=404)
        random_index = random.randint(0, count - 1)
        tool = self.queryset.all()[random_index]
        serializer = self.get_serializer(tool)
        return Response(serializer.data)
        
