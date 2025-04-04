import requests
from django.http import JsonResponse
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from .models import Tool
from .serializers import ToolSerializer


TIMEOUT_SECONDS = 5
MAX_RETRIES = 3

class ToolViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Tool.objects.filter(active=True)
    serializer_class = ToolSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id']

    @method_decorator(ratelimit(key='ip', rate='30/m', method='POST', block=True))
    @method_decorator(ratelimit(key='ip', rate='60/m', method='POST', group='global', block=True))
    @action(detail=False, methods=["post"], url_path="(?P<tool_name>[^/.]+)")
    def proxy_tool(self, request, tool_name):
        """Encaminha a requisição para a API da ferramenta"""

        try: # Valida existencia da ferramenta no banco
            tool = Tool.objects.filter(name=tool_name, active=True).first()
        except Tool.DoesNotExist:
            return JsonResponse({"error": f"Tool '{tool_name}' not found"}, status=404)

        for attempt in range(MAX_RETRIES):
            try:
                response = requests.post(
                    tool.api_url,
                    json=request.data,
                    headers=request.headers,
                    timeout=TIMEOUT_SECONDS
                )
                return JsonResponse(response.json(), status=response.status_code)
            except requests.Timeout:
                if attempt == MAX_RETRIES - 1:
                    return JsonResponse({"error": "Request timeout"}, status=504)
            except requests.RequestException as e:
                if attempt == MAX_RETRIES - 1:
                    return JsonResponse({"error": "Service unavailable"}, status=503)
        
