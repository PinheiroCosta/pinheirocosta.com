from django.views import generic, View
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit
from drf_spectacular.utils import OpenApiExample, extend_schema, OpenApiResponse
from rest_framework import status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import (
    ParametroSistema, 
    AboutMe, 
    RobotsTxt, 
    ProfessionalContactMessage
)
from .serializers import (
    ParametroSistemaSerializer, 
    AboutMeSerializer, 
    MessageSerializer, 
    ProfessionalContactMessageSerializer,
    ProfessionalContactMessageCreateSerializer
)

class ProfessionalContactMessageViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    Endpoint para envio de mensagens através do formulário de contato profissional.

    Permite envio de mensagens públicas que podem ser rastreadas via UTM.
    As mensagens são validadas, armazenas e notificações por email podem ser disparadas.
    """

    permission_classes = [AllowAny]
    queryset = ProfessionalContactMessage.objects.all()
    http_method_names = ["post", "get"]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ProfessionalContactMessageCreateSerializer
        return ProfessionalContactMessageSerializer

    @method_decorator(ratelimit(key='ip', rate='10/m', method='POST', block=False, group='contact'))
    def create(self, request, *args, **kwargs):
        was_limited = getattr(request, 'limited', False)
        if was_limited:
            return Response({'detail': 'Too many requests'}, status=429)
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Listar assuntos disponíveis",
        description="Retorna as opções de assunto válidas para mensagens de contato profissional.",
        responses={
            200: OpenApiResponse(
                response={ "type": "object", "additionalProperties": {"type": "string"} },
                description="Dicionário com as opções disponíveis. Chave/valor para o backend, valor = label exibida no frontend.",
            )
        },
        methods={"GET"},
    )
    @action(detail=False, methods=["get"], url_path="subjects", permission_classes=[AllowAny])
    def list_subjects(self, request):
        """
        Retorna a lista de opções de assunto disponíveis para mensagens de contato profissional.
        """
        choices = dict(ProfessionalContactMessage.SUBJECT_CHOICES)
        return Response(choices)

class RobotsTxtView(View):
    """
    Serve o conteúdo mais recente do robots.txt armazenado no banco.
    Se não houver conteúdo cadastrado, responde com o padrão.
    """

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
    """
    ViewSet somente leitura para acessar os parâmetros de sistema configuráveis.
    """
    queryset = ParametroSistema.objects.all()
    serializer_class = ParametroSistemaSerializer

    @action(detail=False, methods=["get"], url_path="(?P<chave>[^/.]+)")
    def buscar_por_chave(self, request, chave=None):
        """
        Busca um parâmetro de sistema pelo valor da chave.
        Útil para configuração dinâmica no frontend.
        """

        parametro = ParametroSistema.objects.filter(chave=chave).first()
        if parametro:
            return Response({'chave': parametro.chave, 'valor': parametro.valor})
        return Response({'error': 'Parâmetro não encontrado'}, status=404)


class AboutMeViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar informações do dono do site.
    """

    queryset = AboutMe.objects.all()
    serializer_class = AboutMeSerializer
    permission_classes = [AllowAny]
    pagination_class = None

    def get_queryset(self):
        return AboutMe.objects.all()

    def retrieve(self, request, pk=None):
        """
        Retorna os dados do autor. Espera um ID como parâmetro.
        """
        about_me = get_object_or_404(AboutMe, id=pk)
        serializer = AboutMeSerializer(about_me)
        return Response(serializer.data)

    def update(self, request, pk=None):
        """
        Atualiza os dados do autor. Apenas usuários administradores têm permissão.
        """
        if not request.user.is_staff:
            return Response({"error": "Permissão negada."}, status=403)

        about_me = get_object_or_404(AboutMe, id=pk)
        serializer = AboutMeSerializer(about_me, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
