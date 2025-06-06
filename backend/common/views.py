from django.views import generic, View
from django.http import HttpResponse
from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import ParametroSistema, AboutMe, RobotsTxt
from .serializers import ParametroSistemaSerializer, AboutMeSerializer, MessageSerializer


class RobotsTxtView(View):
    def get(self, request, *args, **kwargs):
        try:
            robots = RobotsTxt.objects.latest("last_modified")
            content = robots.content.strip()
        except RobotsTxt.DoesNotExist:
            content = "\n".join([
                "User-Agent: *",
                "Disallow: /admin/",
                "Sitemap: https://www.pinheirocosta.com/sitemap.xml", 
            ])

        response = HttpResponse(content, content_type="text/plain")
        response["Cache-Control"] = "public, max-age=3600"
        return response


class IndexView(generic.TemplateView):
    template_name = "common/index.html"


class RestViewSet(viewsets.ViewSet):
    serializer_class = MessageSerializer

    @extend_schema(
        summary="Check REST API",
        description="This endpoint checks if the REST API is working.",
        examples=[
            OpenApiExample(
                "Successful Response",
                value={
                    "message": "This message comes from the backend. "
                    "If you're seeing this, the REST API is working!"
                },
                response_only=True,
            )
        ],
        methods=["GET"],
    )
    @action(
        detail=False,
        methods=["get"],
        permission_classes=[AllowAny],
        url_path="rest-check",
    )
    def rest_check(self, request):
        serializer = self.serializer_class(
            data={
                "message": "This message comes from the backend. "
                "If you're seeing this, the REST API is working!"
            }
        )
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ParametroSistemaViewSet(viewsets.ReadOnlyModelViewSet): 
    queryset = ParametroSistema.objects.all()
    serializer_class = ParametroSistemaSerializer

    @action(detail=False, methods=["get"], url_path="(?P<chave>[^/.]+)")
    def buscar_por_chave(self, request, chave=None):
        """Busca um parâmetro específico pela chave"""
        parametro = ParametroSistema.objects.filter(chave=chave).first()
        if parametro:
            return Response({'chave': parametro.chave, 'valor': parametro.valor})
        return Response({'error': 'Parâmetro não encontrado'}, status=404)


class AboutMeViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar informaç~oes do dono do site.
    """

    queryset = AboutMe.objects.all()
    serializer_class = AboutMeSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return AboutMe.objects.all()

    def retrieve(self, request, pk=None):
        """
        Retorna os dados do dono do site. Se não existir, retorna erro 404.
        """
        about_me = get_object_or_404(AboutMe, id=pk)
        serializer = AboutMeSerializer(about_me)
        return Response(serializer.data)

    def update(self, request, pk=None):
        """
        Atualiza os dados do dono do site. Apenas administradores podem modificar.
        """
        if not request.user.is_staff:
            return Response({"error": "Permissão negada."}, status=403)

        about_me = get_object_or_404(AboutMe, id=pk)
        serializer = AboutMeSerializer(about_me, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
