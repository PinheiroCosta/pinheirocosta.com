import requests
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Tool
from .serializers import ToolSerializer

class ToolViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Tool.objects.all()
    serializer_class = ToolSerializer

    def list(self, request):
        tools = Tool.objects.filter(active=True)
        serializer = self.get_serializer(tools, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["post"], url_path="(?P<tool_name>[^/.]+)")
    def proxy_tool(self, request, tool_name):
        """Encaminha a requisição para a API da ferramenta"""

        tool = Tool.objects.filter(name=tool_name, active=True).first()
        if not tool:
            return JsonResponse({"error": f"Tool '{tool_name}' not found"}, status=404)

        api_url = tool.api_url
        try:
            response = requests.post(api_url, json=request.data, headers=request.headers)
            return JsonResponse(response.json(), status=response.status_code)
        except requests.exceptions.RequestException as e:
            return JsonResponse({"error": f"Failed to connect to '{tool_name}' API", "details": str(e)}, status=500)

