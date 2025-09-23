from django.contrib import admin
from .models import Parceria, Servico, PedidoServico, PedidoItem, TicketSuporte, ContratoServico, ServicoContratado, CupomPromocional
from .forms import ParceriaForm, PedidoServicoForm, PedidoItemForm, ServicoContratadoForm


class ServicoContratadoInline(admin.TabularInline):
    model = ServicoContratado
    form = ServicoContratadoForm
    extra = 0
    fields = ('servico', 'data_inicio', 'data_fim', 'recorrente')
    readonly_fields = ('data_inicio',)
    can_delete = True

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


class PedidoItemInline(admin.TabularInline):
    model = PedidoItem
    form = PedidoItemForm
    extra = 0
    fields = ('servico', 'data_renovacao', 'recorrente', 'periodo_gratuito')
    readonly_fields = ('data_renovacao',)

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


class PedidoServicoInline(admin.TabularInline):
    model = PedidoServico
    extra = 0
    fields = ('status_pedido_servico',)
    can_delete = False

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request, obj=None):
        return request.user.is_superuser


class TicketSuporteInline(admin.TabularInline):
    model = TicketSuporte
    extra = 0
    fields = ('titulo', 'descricao', 'status_ticket_suporte',)
    can_delete = False

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


class ContratoServicoInline(admin.TabularInline):
    model = ContratoServico
    extra = 0
    fields = ('parceria', 'data_inicio', 'data_fim', 'ativo')
    can_delete = False
    readonly_fields = ('parceria', 'data_inicio',)

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


@admin.register(Parceria)
class ParceriaAdmin(admin.ModelAdmin):
    form = ParceriaForm
    list_display = ('nome', 'categoria', 'dominio')
    inlines = [ContratoServicoInline, PedidoServicoInline, TicketSuporteInline]


@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco_base')
    search_fields = ('nome',)


@admin.register(PedidoServico)
class PedidoServicoAdmin(admin.ModelAdmin):
    form = PedidoServicoForm
    list_display = ('parceria', 'status_pedido_servico')
    list_filter = ('status_pedido_servico',)
    inlines = [PedidoItemInline]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('parceria')

@admin.register(TicketSuporte)
class TicketSuporteAdmin(admin.ModelAdmin):
    list_display = (
        'tipo_ticket_suporte',
        'titulo',
        'descricao',
        'status_ticket_suporte',
        'prazo_entrega',
    )
    list_filter = ('status_ticket_suporte',)

    def get_readonly_fields(self, request, obj=None):
        # Se for superuser, pode editar tudo
        if request.user.is_superuser:
            return
        # Caso contrário, restringe
        return ("data_criacao", "prazo_entrega", "status_ticket_suporte")


@admin.register(ContratoServico)
class ContratoServicoAdmin(admin.ModelAdmin):
    list_display = ('parceria', 'data_inicio', 'data_fim', 'ativo')
    list_filter = ('ativo',)
    search_fields = ('parceria__nome', 'servicos_contratados__servico__nome')
    date_hierarchy = 'data_inicio'
    inlines = [ServicoContratadoInline]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('parceria')


@admin.register(CupomPromocional)
class CupomPromocionalAdmin(admin.ModelAdmin):
    list_display = ('cupom', 'tipo', 'valor', 'validade', 'ativo', 'uso_unico', 'data_uso')
    list_filter = ('tipo', 'ativo', 'uso_unico')
    search_fields = ('cupom',)
    readonly_fields = ('data_uso',)
    date_hierarchy = 'validade'



@admin.register(ServicoContratado)
class ServicoContratadoAdmin(admin.ModelAdmin):
    form = ServicoContratadoForm
    list_display = (
        'servico',
        'contrato_servico',
        'data_inicio',
        'data_fim',
        'recorrente',
    )
    list_filter = ('recorrente',)
    search_fields = ('servico__nome', 'contrato_servico__parceria__nome')

    readonly_fields = ('contrato_servico',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'servico', 'contrato_servico'
        )

