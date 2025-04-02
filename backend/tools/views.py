from rest_framework import viewsets
from rest_framework.response import Response
from .models import Tool
from .serializers import ToolSerializer

class ToolViewSet(viewsets.ModelViewSet):
    queryset = Tool.objects.all()
    serializer_class = ToolSerializer

    def list(self, request):
        tools = Tool.objects.filter(active=True)
        serializer = self.get_serializer(tools, many=True)
        return Response(serializer.data)

