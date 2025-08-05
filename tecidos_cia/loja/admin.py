# loja/admin.py
from django.contrib import admin
from .models import Categoria, Tecido, Pedido, ItemPedido

class TecidoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'preco_por_metro', 'estoque_metros', 'disponivel', 'destaque')
    list_filter = ('categoria', 'disponivel', 'destaque')
    search_fields = ('nome', 'descricao')

class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    readonly_fields = ('tecido', 'quantidade_metros', 'get_total')
    extra = 0

class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'data_pedido', 'completo', 'get_total_carrinho')
    list_filter = ('completo', 'data_pedido')
    inlines = [ItemPedidoInline]

admin.site.register(Categoria)
admin.site.register(Tecido, TecidoAdmin)
admin.site.register(Pedido, PedidoAdmin)