from django.contrib import admin
from .models import Ingrediente, Produto, ProdutoIngrediente, Funcionario, Pedido, PedidoProduto, EnderecoEntrega, Avaliacao

# Register your models here.
admin.site.register(Ingrediente)
admin.site.register(Produto)
admin.site.register(ProdutoIngrediente)
admin.site.register(Funcionario)
admin.site.register(Pedido)
admin.site.register(PedidoProduto)
admin.site.register(EnderecoEntrega)
admin.site.register(Avaliacao)

