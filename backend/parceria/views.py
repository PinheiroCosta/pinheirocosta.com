from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.http import Http404
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from .models import *
from .serializers import *
from . import services


class BaseClienteViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        model = self.queryset.model

        if model in [ContratoServico, PedidoServico]:
            return model.objects.filter(
                parceria__membros__usuario=user,
                parceria__membros__ativo=True
            )
        else:
            raise ImproperlyConfigured(f"Queryset não configurado para {model.__name__}")

    def get_object(self):
        """
        A visibilidade e o acesso a TicketsSuporte, PedidoServico e ContratoServico
        são estritamente determinados pela relação parceria.membros.
        Usuários sem vínculo ativo com a parceria do recurso recebem 404 por design,
        garantindo isolamento entre clientes. Em cenários de operação cruzada
        entre parcerias, será necessário adicionar o operador como membro da
        parceria-alvo ou fornecer credenciais específicas para aquela parceria.
        """
        obj = super().get_object()
        user = self.request.user

        if hasattr(obj, "parceria"):
            if not obj.parceria.membros.filter(usuario=user, ativo=True).exists():
                raise PermissionDenied("Acesso negado.")
        elif hasattr(obj, "pedido") and hasattr(obj.pedido, "parceria"):
            if not obj.pedido.parceria.membros.filter(usuario=user, ativo=True).exists():
                raise PermissionDenied("Acesso negado.")

        return obj

    def perform_create(self, serializer):
        parceria = Parceria.objects.filter(
            membros__usuario=self.request.user,
            membros__ativo=True
        ).first()
        if not parceria:
            raise PermissionDenied("Usuário não está vinculado a uma parceria.")
        serializer.save(parceria=parceria)


class ServicoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Servico.objects.all()
    serializer_class = ServicoSerializer
    permission_classes = [permissions.IsAuthenticated]


class PedidoServicoViewSet(BaseClienteViewSet):
    queryset = PedidoServico.objects.all()
    serializer_class = PedidoServicoSerializer

    @action(detail=True, methods=["post"], url_path="concluir")
    def concluir(self, request, pk=None):
        pedido = self.get_object()

        # Permissão: garantir que o pedido pertence à parceria do usuário
        parceria = Parceria.objects.filter(
            membros__usuario=request.user,
            membros__ativo=True
        ).first()

        if pedido.parceria != parceria:
            return Response(
                {"detail": "Acesso não autorizado ao pedido."},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            pedido = services.concluir_pedido(pedido)
        except ValidationError as e:
            return Response({"detail": e.message}, status=400)

        serializer = self.get_serializer(pedido)
        return Response(serializer.data, status=200)

    @action(detail=True, methods=["post"], url_path="cancelar")
    def cancelar(self, request, pk=None):
        pedido = self.get_object()

        parceria = Parceria.objects.filter(
            membros__usuario=request.user,
            membros__ativo=True
        ).first()

        if pedido.parceria != parceria:
            return Response(
                {"detail": "Acesso não autorizado ao pedido."},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            pedido = services.cancelar_pedido(pedido)
        except ValidationError as e:
            return Response({"detail": e.message}, status=400)

        serializer = self.get_serializer(pedido)
        return Response(serializer.data, status=200)

    def perform_create(self, serializer):
        parceria = Parceria.objects.filter(
            membros__usuario=self.request.user,
            membros__ativo=True
        ).first()

        itens_raw = self.request.data.get("itens", [])

        itens = []
        # Cria itens se vierem no request
        for item_data in itens_raw:
            servico = Servico.objects.get(pk=item_data["servico"])
            itens.append({
                "servico": servico,
                "recorrente": item_data.get("recorrente", False),
                "data_renovacao": item_data.get("data_renovacao"),
            })

        pedido = services.criar_pedido(
            parceria=parceria,
            itens=itens,
            status_pedido_servico=self.request.data.get("status_pedido_servico"),
        )

        serializer.instance = pedido


    def destroy(self, request, *args, **kwargs):
        return Response(
            {'detail': 'Exclusão de pedidos não é permitida'},
            status=status.HTTP_403_FORBIDDEN
        )


class ContratoServicoViewSet(BaseClienteViewSet):
    queryset = ContratoServico.objects.all()
    serializer_class = ContratoServicoSerializer

    def destroy(self, request, *args, **kwargs):
        return Response(
            {'detail': 'Exclusão de contratos não é permitida'},
            status=status.HTTP_403_FORBIDDEN
        )



class TicketSuporteViewSet(BaseClienteViewSet):
    queryset = TicketSuporte.objects.all()
    serializer_class = TicketSuporteSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=["post"], url_path="responder")
    def responder(self, request, pk=None):
        ticket = self.get_object()

        parceria = Parceria.objects.filter(
            membros__usuario=request.user,
            membros__ativo=True
        ).first()

        if ticket.parceria != parceria:
            return Response(
                {"detail": "Acesso não autorizado ao ticket."},
                status=status.HTTP_403_FORBIDDEN
            )

        conteudo = request.data.get("conteudo")
        if not conteudo:
            return Response({"detail": "Campo 'conteudo' é obrigatório."}, status=400)

        try:
            mensagem = services.responder_ticket(
                ticket=ticket,
                usuario=request.user,
                conteudo=conteudo,
            )
        except ValidationError as e:
            return Response({"detail": e.message}, status=400)

        serializer = self.get_serializer(ticket)
        return Response(serializer.data, status=200)


    def get_queryset(self):
        user = self.request.user
        return (
            TicketSuporte.objects.filter(parceria__proprietario=user)
            | TicketSuporte.objects.filter(parceria__membros__usuario=user, parceria__membros__ativo=True)
        ).distinct()

    def perform_create(self, serializer):
        parceria = Parceria.objects.filter(
            proprietario=self.request.user
        ).first() or Parceria.objects.filter(
            membros__usuario=self.request.user,
            membros__ativo=True
        ).first()

        if not parceria:
            raise PermissionDenied("Usuário não está vinculado a uma parceria.")

        titulo = serializer.validated_data.get("titulo")
        descricao = serializer.validated_data.get("descricao")
        tipo_ticket = serializer.validated_data.get("tipo_ticket_suporte")

        ticket = services.criar_ticket(
            parceria=parceria,
            tipo_ticket=tipo_ticket,
            titulo=titulo,
            descricao=descricao
        )

        serializer.instance = ticket

    def destroy(self, request, *args, **kwargs):
        return Response(
            {'detail': 'Exclusão de Tickets não é permitida.'},
            status=status.HTTP_403_FORBIDDEN
        )

