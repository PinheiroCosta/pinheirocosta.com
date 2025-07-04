from django.contrib import admin
from .models import Parceria, Servico, PedidoServico, SugestaoServico
from .forms import ParceriaForm


@admin.register(Parceria)
class ParceriaAdmin(admin.ModelAdmin):
    form = ParceriaForm
    list_display = ('user', 'nome_projeto', 'dominio', 'data_criacao', 'status_servicos')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(parceria__user=request.user)

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser or obj is None:
            return True
        return obj.parceria.user == request.user

    def status_servicos(self, obj):
        ativos = obj.pedidos.filter(status='em_andamento').count()
        pendentes = obj.pedidos.filter(status='pendente').count()
        return f"{ativos} ativos / {pendentes} pendentes"
    status_servicos.short_description = "Serviços"


@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco')
    search_fields = ('nome',)


@admin.register(PedidoServico)
class PedidoServicoAdmin(admin.ModelAdmin):
    list_display = ('parceria', 'servico', 'status', 'data_pedido', 'vencimento', 'desconto')
    list_filter = ('status', 'servico')
    date_hierarchy = 'data_pedido'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(parceria__user=request.user)

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser or obj is None:
            return True
        return obj.parceria.user == request.user

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "parceria" and not request.user.is_superuser:
            kwargs["queryset"] = Parceria.objects.filter(user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def save_model(self, request, obj, form, change):
        if not change and not request.user.is_superuser:
            obj.parceria = Parceria.objects.get(user=request.user)
        super().save_model(request, obj, form, change)


@admin.register(SugestaoServico)
class SugestaoServicoAdmin(admin.ModelAdmin):
    list_display = ('parceria', 'titulo', 'descricao', 'data', 'status')
    list_filter = ('status', 'data')
    date_hierarchy = 'data'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(parceria__user=request.user)

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser or obj is None:
            return True
        return obj.parceria.user == request.user

