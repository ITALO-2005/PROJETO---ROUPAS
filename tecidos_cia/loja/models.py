# loja/models.py
from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal


class Categoria(models.Model):
    nome = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Categorias"

    def __str__(self):
        return self.nome

class Tecido(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField()
    preco_por_metro = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    imagem = models.ImageField(upload_to='tecidos/', blank=True, null=True)
    estoque_metros = models.FloatField()
    disponivel = models.BooleanField(default=True)
    destaque = models.BooleanField(default=False) # Adicionei para a home

    def __str__(self):
        return self.nome

class Pedido(models.Model):
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    data_pedido = models.DateTimeField(auto_now_add=True)
    completo = models.BooleanField(default=False)

    def __str__(self):
        return f'Pedido {self.id} de {self.cliente.username}'

    @property
    def get_total_carrinho(self):
        itens_pedido = self.itempedido_set.all()
        total = sum([item.get_total for item in itens_pedido])
        return total

class ItemPedido(models.Model):
    tecido = models.ForeignKey(Tecido, on_delete=models.CASCADE)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    # ALTERAÇÃO AQUI: Trocamos FloatField por DecimalField
    quantidade_metros = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('1.00'))
    data_adicao = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        # A linha da multiplicação agora funciona perfeitamente
        total = self.tecido.preco_por_metro * self.quantidade_metros
        return total