from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.usuario_principal, name='usuario'),
    path('usuario_cadastro/', views.usuario_cadastro, name='usuario_cadastro'),
    path('usuario_login/', views.usuario_login, name='usuario_login'),
    path('usuario_perfil/', views.usuario_perfil, name='usuario_perfil'),
    path('usuario_principal/', views.usuario_principal, name='usuario_principal'),
    path('usuario_pesquisa_produto', views.usuario_pesquisa_produto, name='usuario_pesquisa_produto'),
    path('usuario_logout/', views.usuario_logout, name='usuario_logout'),
    path('usuario_carrinho/', views.usuario_carrinho, name='usuario_carrinho'),
    path('usuario_checkout/', views.usuario_checkout, name='usuario_checkout'),
    path('usuario_update_item/', views.update_item, name='usuario_update_item'),
    path('usuario_processar_pedido/', views.processa_pedido, name='usuario_processar_pedido'),
    path('usuario_produto/<int:id_produto>/', views.usuario_produto, name='usuario_produto'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)