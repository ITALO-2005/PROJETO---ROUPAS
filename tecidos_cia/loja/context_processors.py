# loja/context_processors.py
from .models import Pedido

def carrinho(request):
    if request.user.is_authenticated:
        pedido, created = Pedido.objects.get_or_create(cliente=request.user, completo=False)
        total_itens = pedido.itempedido_set.count()
        return {'total_itens_carrinho': total_itens}
    return {'total_itens_carrinho': 0}