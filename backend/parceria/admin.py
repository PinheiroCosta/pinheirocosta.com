from django.contrib import admin
from .models import Parceria, Servico, PedidoServico
from .forms import ParceriaForm


@admin.register(Parceria)
class ParceriaAdmin(admin.ModelAdmin):
    form = ParceriaForm
    list_display = ('user', 'nome_projeto', 'dominio', 'data_criacao', 'status_servicos')

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
