# loja/urls.py
from django.urls import path
from . import views
# Importa as views de autenticação do Django
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Páginas Públicas
    path('', views.home, name='home'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('produto/<int:id>/', views.detalhes_produto, name='detalhes_produto'),
    
    # Carrinho
    path('carrinho/', views.carrinho, name='carrinho'),
    path('adicionar_ao_carrinho/', views.adicionar_ao_carrinho, name='adicionar_ao_carrinho'),
    path('remover_do_carrinho/', views.remover_do_carrinho, name='remover_do_carrinho'),
    
    # Sistema de Usuário
    path('cadastro/', views.register, name='register'), # <-- ROTA ADICIONADA
    path('login/', auth_views.LoginView.as_view(template_name='loja/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # (As outras views de senha podem ser adicionadas de forma similar se necessário)
]