from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # TELAS #

    # PRINCIPAL #
    path('', views.gerente_principal, name='gerenciamento'),
    path('gerente_perfil/', views.gerente_perfil, name='gerente_perfil'),
    path('gerente_principal/', views.gerente_principal, name='gerente_principal'),

    # PEDIDOS # 
    path('gerente_lista_pedidos/', views.gerente_lista_pedidos, name='gerente_lista_pedidos'),
    path('nota_pedido/<int:id_pedido>', views.nota_pedido, name='nota_pedido'),
    path('gerente_excluir_pedido/<int:id_pedido>/', views.gerente_excluir_pedido, name='gerente_excluir_pedido'),

    # CLIENTES #
    path('gerente_lista_clientes/' , views.gerente_lista_clientes, name='gerente_lista_clientes'),

    # FUNCIONÁRIOS #
    path('gerente_lista_funcionarios/', views.gerente_lista_funcionarios, name='gerente_lista_funcionarios'),
    path('gerente_add_funcionario/', views.gerente_add_funcionario, name='gerente_add_funcionario'),
    path('gerente_att_funcionario/<int:id_funcionario>', views.gerente_att_funcionario, name='gerente_att_funcionario'),
    path('gerente_excluir_funcionario/<int:funcionario_id>/', views.gerente_excluir_funcionario, name='gerente_excluir_funcionario'),

    # PRODUTOS #
    path('gerente_add_produto/', views.gerente_add_produto, name='gerente_add_produto'),
    path('gerente_att_produto/<int:id_produto>', views.gerente_att_produto, name='gerente_att_produto'),
    path('gerente_produto/<int:id_produto>/', views.gerente_produto, name='gerente_produto'),
    path('gerente_pesquisa_produto/', views.gerente_pesquisar_produto, name='gerente_pesquisa_produto'), 
    path('gerente_excluir_produto/<int:id_produto>/', views.gerente_excluir_produto, name='gerente_excluir_produto'),

    # FUNÇÕES DE DADOS #
    path('dados_funcionario/', views.dados_funcionario, name='dados_funcionario'),
    path('dados_produto/', views.dados_produto, name='dados_produto'),
    path('dados_pedido/', views.dados_pedido, name='dados_pedido'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)