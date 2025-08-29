from django.contrib import admin
from .models import Parceria, Servico, PedidoServico, TicketSuporte, ContratoServico
from .forms import ParceriaForm, PedidoServicoForm


class PedidoServicoInline(admin.TabularInline):
    model = PedidoServico
    extra = 0
    fields = ('servico', 'status_pedido_servico', 'data_pedido', 'vencimento', 'desconto')
    can_delete = False
    readonly_fields = ('data_pedido',)

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request, obj=None):
        return request.user.is_superuser


class TicketSuporteInline(admin.TabularInline):
    model = TicketSuporte
    extra = 0
    fields = ('titulo', 'descricao', 'resposta', 'status_ticket_suporte', 'data_criacao',)
    can_delete = False

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


class ContratoServicoInline(admin.TabularInline):
    model = ContratoServico
    extra = 0
    fields = ('servico', 'data_inicio', 'data_fim', 'cancelado')
    can_delete = False
    readonly_fields = ('data_inicio',)

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


@admin.register(Parceria)
class ParceriaAdmin(admin.ModelAdmin):
    form = ParceriaForm
    list_display = ('nome_projeto', 'dominio', 'data_criacao')
    inlines = [ContratoServicoInline, PedidoServicoInline, TicketSuporteInline]


@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco')
    search_fields = ('nome',)


@admin.register(PedidoServico)
class PedidoServicoAdmin(admin.ModelAdmin):
    form = PedidoServicoForm
    list_display = ('servico', 'status_pedido_servico', 'contrato', 'data_pedido', 'vencimento', 'desconto')
    list_filter = ('status_pedido_servico', 'servico', 'contrato')
    date_hierarchy = 'data_pedido'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('servico', 'parceria', 'contrato')


@admin.register(TicketSuporte)
class TicketSuporteAdmin(admin.ModelAdmin):
    list_display = ('tipo_ticket_suporte', 'titulo', 'descricao', 'status_ticket_suporte', 'data_criacao', 'prazo_entrega', 'resposta')
    list_filter = ('status_ticket_suporte', 'data_criacao')
    date_hierarchy = 'data_criacao'


@admin.register(ContratoServico)
class ContratoServicoAdmin(admin.ModelAdmin):
    list_display = ('parceria', 'servico', 'data_inicio', 'data_fim', 'cancelado')
    list_filter = ('servico', 'cancelado')
    search_fields = ('parceria__nome_projeto', 'servico__nome')
    date_hierarchy = 'data_inicio'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('servico', 'parceria', 'contrato')
