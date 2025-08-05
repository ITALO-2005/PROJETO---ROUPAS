from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from .models import Tecido, Categoria, Pedido, ItemPedido
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json

def home(request):
    tecidos_destaque = Tecido.objects.filter(disponivel=True, destaque=True)
    context = {'tecidos_destaque': tecidos_destaque}
    return render(request, 'loja/home.html', context)

def catalogo(request):
    categoria_id = request.GET.get('categoria')
    if categoria_id:
        tecidos = Tecido.objects.filter(disponivel=True, categoria_id=categoria_id)
    else:
        tecidos = Tecido.objects.filter(disponivel=True)
    
    categorias = Categoria.objects.all()
    context = {'tecidos': tecidos, 'categorias': categorias}
    return render(request, 'loja/catalogo.html', context)

def detalhes_produto(request, id):
    tecido = get_object_or_404(Tecido, id=id)
    context = {'tecido': tecido}
    return render(request, 'loja/detalhes_produto.html', context)

@login_required
def carrinho(request):
    pedido, created = Pedido.objects.get_or_create(cliente=request.user, completo=False)
    itens_do_carrinho = pedido.itempedido_set.all()
    context = {'itens_do_carrinho': itens_do_carrinho, 'pedido': pedido}
    return render(request, 'loja/carrinho.html', context)

@login_required
def adicionar_ao_carrinho(request):
    data = json.loads(request.body)
    produto_id = data['produtoId']
    metragem = float(data['metragem'])
    
    tecido = Tecido.objects.get(id=produto_id)
    pedido, created = Pedido.objects.get_or_create(cliente=request.user, completo=False)
    
    item, created = ItemPedido.objects.get_or_create(pedido=pedido, tecido=tecido)
    item.quantidade_metros = metragem
    item.save()
    
    return JsonResponse('Item foi adicionado', safe=False)

@login_required
def remover_do_carrinho(request):
    data = json.loads(request.body)
    item_id = data['itemId']
    item = ItemPedido.objects.get(id=item_id)
    item.delete()
    return JsonResponse('Item foi removido', safe=False)

# ADICIONE ESTA NOVA FUNÇÃO NO FINAL DO ARQUIVO
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save() # Salva o novo usuário no banco de dados
            login(request, user) # Faz o login automático do usuário após o cadastro
            messages.success(request, "Cadastro realizado com sucesso!")
            return redirect('home') # Redireciona para a página inicial
        else:
            messages.error(request, "Não foi possível realizar o cadastro. Verifique os erros abaixo.")
    else:
        form = UserCreationForm()
        
    context = {'form': form}
    return render(request, 'loja/register.html', context)