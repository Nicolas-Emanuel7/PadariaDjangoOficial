import datetime
from django.utils import timezone
import json
from django.http import FileResponse, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from fpdf import FPDF
from io import BytesIO

from gerenciamento.models import Funcionario, Ingrediente, Pedido, PedidoProduto, Produto, ProdutoIngrediente, Avaliacao
from usuario.models import Usuario

#Verificador de permissão
def verifica_permissao(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.permissao:
            return func(request, *args, **kwargs)
        else:
            return redirect('usuario_cadastro')
    return wrapper

#telas
@verifica_permissao
def gerente_principal(request):
    produtos_list = Produto.objects.all()
    return render(request, 'gerente_principal.html', {'produtos': produtos_list})

@verifica_permissao
def gerente_lista_pedidos(request):
     # Obtém a data do primeiro dia do mês atual
    primeiro_dia_mes_atual = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    # Obtém todos os pedidos do mês atual
    pedidos_mes_atual = Pedido.objects.filter(data__gte=primeiro_dia_mes_atual)

    # Calcula a soma do valor de todos os pedidos do mês atual
    soma_valor_pedidos_mes_atual = sum(pedido.valor_final for pedido in pedidos_mes_atual)
    pedidos_list = Pedido.objects.order_by('-id_pedido')
    return render(request, 'gerente_pedidos.html', {'pedidos': pedidos_list , 'soma_valor_pedidos_mes_atual': soma_valor_pedidos_mes_atual})

@verifica_permissao
def gerente_lista_clientes(request):
    if request.method == "GET":
        clientes_list = Usuario.objects.order_by('-date_joined')
        return render(request, 'gerente_clientes.html', {'clientes': clientes_list})
    else:
        return render(request, 'gerente_clientes.html')

@verifica_permissao
def gerente_lista_funcionarios(request):
    funcionarios_list = Funcionario.objects.all()
    return render(request, 'gerente_funcionarios.html', {'funcionarios': funcionarios_list})

@verifica_permissao
def gerente_perfil(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('nome')
        user.last_name = request.POST.get('sobrenome')
        user.telefone = request.POST.get('telefone')
        user.email = request.POST.get('email')
        user.password = (request.POST.get('senha'))
        user.username = (request.POST.get('nome'))
        user.permissao = True
        user.save()
        return redirect('gerente_perfil')
    return render(request, 'gerente_perfil.html')

@verifica_permissao
def gerente_produto(request, id_produto):
    categorias = Produto.CATEGORIA_CHOICES
    produto = get_object_or_404(Produto, id_produto=id_produto)
    media_avaliacoes = Avaliacao.calcular_media_avaliacoes(produto)
    ingredientes_produto = produto.ingredientes.all()

    avaliacoes = Avaliacao.objects.filter(produto=produto) 

    contexto = {'produto': produto,  'avaliacoes': avaliacoes, 'media_avaliacoes': media_avaliacoes, 'ingredientes_produto': ingredientes_produto, 'categorias':categorias}
    return render(request, 'gerente_produto.html', contexto)


    
#funções de adicionar

@verifica_permissao   
def gerente_add_funcionario(request):
    funcionarios_list = Funcionario.objects.all()
    if request.method == "GET":
        return render(request, 'gerente_funcionarios.html', {'funcionarios': funcionarios_list})
    elif request.method == "POST":
        nome_funcionario = request.POST.get('nome_funcionario')
        telefone_funcionario = request.POST.get('telefone_funcionario')
        cargo = request.POST.get('cargo')
        salario = request.POST.get('salario')

        funcionario = Funcionario.objects.filter(nome_funcionario=nome_funcionario, telefone_funcionario=telefone_funcionario, cargo=cargo, salario=salario)

        if funcionario:
            return JsonResponse({'status': '500'})
        else:
            funcionario = Funcionario.objects.create(nome_funcionario=nome_funcionario, telefone_funcionario=telefone_funcionario, cargo=cargo, salario=salario)
            funcionario.save()

        return render(request, 'gerente_funcionarios.html', {'funcionarios': funcionarios_list})

@verifica_permissao    
def gerente_add_produto(request):
    categorias = Produto.CATEGORIA_CHOICES
    if request.method == 'POST':
        nome_produto = request.POST.get('nome_produto')
        descricao = request.POST.get('descricao')
        preco = request.POST.get('preco')
        categoria = request.POST.get('categoria')
        imagem = request.FILES.get('imagem')
        nomeIngredientes = request.POST.getlist('nome_ingrediente')
        unidadeMedidas = request.POST.getlist('unidade_Medida')

        # Salvando os dados do produto no banco de dados
        produto = Produto.objects.create(nome_produto=nome_produto, descricao=descricao, preco=preco, categoria=categoria, imagem=imagem)
        produto.save()
        print(produto)

        for nomeIngrediente, unidadeMedida in zip(nomeIngredientes, unidadeMedidas):
            ingrediente, created = Ingrediente.objects.get_or_create(nome_ingrediente=nomeIngrediente, unidade_Medida=unidadeMedida)
            produto_ingrediente = ProdutoIngrediente.objects.create(produto=produto, ingrediente=ingrediente)
            produto_ingrediente.save()
            print(ingrediente)

        # Redirecionar para alguma página de sucesso ou para a página inicial
        return redirect('gerente_principal')

    # Se o método da requisição não for POST, renderizar o formulário vazio
    return render(request, 'gerente_add_produto.html', {'categorias': categorias})
        
        
# FUNÇÕES DE BUSCA

@verifica_permissao
def gerente_pesquisar_produto(request):
    termo_pesquisa = request.GET.get('Pesquisar', '')
    resultados = Produto.objects.filter(nome_produto__icontains=termo_pesquisa)
    contexto = {'resultados': resultados, 'termo_pesquisa': termo_pesquisa}
    return render(request, 'gerente_pesquisa_produto.html', contexto)

#funções de atualizar
@verifica_permissao
def gerente_att_produto(request, id_produto):
    if request.method == 'POST':
        produtoAtt = Produto.objects.get(id_produto=id_produto)
        print(produtoAtt)
        produtoAtt.nome_produto = request.POST.get('nome_produto')
        produtoAtt.descricao = request.POST.get('descricao')
        produtoAtt.preco = request.POST.get('preco')
        produtoAtt.categoria = request.POST.get('categoria')
        produtoAtt.save()

        ProdutoIngrediente.objects.filter(produto=produtoAtt).delete()

        nomeIngredientes = request.POST.getlist('nome_ingrediente')
        unidadeMedidas = request.POST.getlist('unidade_Medida')

        for nomeIngrediente, unidadeMedida in zip(nomeIngredientes, unidadeMedidas):
            ingrediente, created = Ingrediente.objects.get_or_create(nome_ingrediente=nomeIngrediente, unidade_Medida=unidadeMedida)
            produto_ingrediente = ProdutoIngrediente.objects.create(produto=produtoAtt, ingrediente=ingrediente)
            produto_ingrediente.save()
            print(ingrediente)

        return redirect('gerente_produto', id_produto=id_produto)
    
    return redirect('gerente_produto', id_produto=id_produto)

@verifica_permissao
def gerente_att_funcionario(request):
    if request.method == 'POST':
        id_funcionario = request.POST.get('id_funcionario')
        print(id_funcionario)
        funcionarioAtt = Funcionario.objects.get(id_funcionario=id_funcionario)
        print(funcionarioAtt)
        funcionarioAtt.nome_funcionario = request.POST.get('nome_funcionario')
        funcionarioAtt.telefone_funcionario = request.POST.get('telefone_funcionario')
        funcionarioAtt.cargo = request.POST.get('cargo')
        funcionarioAtt.salario = request.POST.get('salario')
        print(funcionarioAtt)
        funcionarioAtt.save()
        return redirect('gerente_lista_funcionarios')
    return redirect('gerente_lista_funcionarios')
    
#funções de deletar

@verifica_permissao  
def gerente_excluir_produto(request, id_produto):
    produto = Produto.objects.get(id_produto=id_produto)
    print(produto)
    produto.delete()
    return redirect('gerente_principal')

@verifica_permissao
def gerente_excluir_pedido(request, id_pedido):
    pedido = Pedido.objects.get(id_pedido=id_pedido)
    print(pedido)
    pedido.delete()
    return redirect('gerente_lista_pedidos')

@verifica_permissao
def gerente_excluir_funcionario(request, id_funcionario):
    funcionario = Funcionario.objects.get(id_funcionario=id_funcionario)
    print(funcionario)
    funcionario.delete()
    return redirect('gerente_lista_funcionarios')

@verifica_permissao
def gerente_excluir_ingrediente(request, id_ingrediente, id_produto):
    produto = Produto.objects.get(id_produto=id_produto)
    ingrediente = Ingrediente.objects.get(id_ingrediente=id_ingrediente)
    produto_ingrediente = ProdutoIngrediente.objects.get(produto=produto, ingrediente=ingrediente)
    produto_ingrediente.delete()
    return redirect('gerente_produto', id_produto=id_produto)

#funções de dados

@verifica_permissao
def dados_pedido(request):
    id_pedido = request.POST.get('id_pedido')
    pedido = Pedido.objects.filter(id_pedido=id_pedido)
    pedido_json = json.loads(serializers.serialize('json', pedido))[0]['fields']
    pedido_id = json.loads(serializers.serialize('json', pedido))[0]['pk']
    data = {'pedido': pedido_json, 'pedido_id': pedido_id}
    return JsonResponse(data)

@verifica_permissao
def dados_produto(request):
    id_produto = request.POST.get('id_produto')
    produto = Produto.objects.filter(id_produto=id_produto).first()
    print(produto)
    if produto:
        # Obtém todos os ingredientes associados ao produto
        ingredientes = produto.get_ingredientes
        
        # Serializa os ingredientes manualmente para um formato JSON válido
        ingredientes_json = [
            {
                'id_ingrediente': ingrediente.id_ingrediente,
                'nome_ingrediente': ingrediente.nome_ingrediente,
                'unidade_Medida': ingrediente.unidade_Medida,
            }
            for ingrediente in ingredientes
        ]
        
        # Retorna a lista de ingredientes como resposta JSON
        return JsonResponse({'ingredientes': ingredientes_json, 'id_produto':produto.id_produto})
    else:
        # Se o produto não for encontrado, retorna uma resposta de erro
        return JsonResponse({'error': 'Produto não encontrado'}, status=404)

@verifica_permissao
def dados_funcionario(request):
    if request.method == "POST":
        id_funcionario = request.POST.get('id_funcionario')
        print(id_funcionario)
        funcionario = Funcionario.objects.filter(id_funcionario=id_funcionario).first()  # Use .first() para obter apenas um objeto
        if funcionario:
            data = {
                'id_funcionario': funcionario.id_funcionario,
                'nome_funcionario': funcionario.nome_funcionario,
                'telefone_funcionario': funcionario.telefone_funcionario,
                'cargo': funcionario.cargo,
                'salario': funcionario.salario,
            }
            print(data)
            return JsonResponse(data)
        else:
            return JsonResponse({'error': 'Funcionário não encontrado'}, status=404)

#Não usa a verificação, pois é usada por usuários e gerentes       
def dados_perfil(request):
    if request.method == "POST":
        user = request.user
        data = {
            'nome': user.first_name,
            'sobrenome': user.last_name,
            'telefone': user.telefone,
            'email': user.email,
            'senha': user.password,
        }
        print(data)
        return JsonResponse(data)
        
#Função de exclusão de perfil
def excluir_perfil(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        print('Usuário excluído com sucesso!')
        return render(request, 'usuario_cadastro.html')

#detalhes de pedido

def nota_pedido(request, id_pedido):
    pedido = get_object_or_404(Pedido, id_pedido=id_pedido)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 12)
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(35, 10, 'Cliente: ', 1, 0, 'L', 1)
    pdf.cell(0, 10, f'{pedido.cliente.first_name} {pedido.cliente.last_name}', 1, 1, 'L', 1)
    pdf.cell(35, 10, 'Data da Compra: ', 1, 0, 'L', 1)
    pdf.cell(0, 10, f'{pedido.data}', 1, 1, 'L', 1)

    pdf.cell(35, 10, 'Produtos: ', 1, 0, 'L', 1)

    pedido_produtos = PedidoProduto.objects.filter(pedido=pedido)
    for i, pedido_produto in enumerate(pedido_produtos):
        produto = pedido_produto.produto
        quantidade = pedido_produto.quantidade_comprada

        pdf.cell(0, 10, f'{produto.nome_produto} - Quantidade: {quantidade} - Preço: R${produto.preco}', 1, 1, 'L', 1)
        if not i == len(pedido_produtos) - 1:
            pdf.cell(35, 10, '', 0, 0, 'L', 0)

    pdf.cell(35, 10, 'Valor Total: ', 1, 0, 'L', 1)
    pdf.cell(0, 10, f'R${pedido.get_carrinho_total}', 1, 1, 'L', 1)
    
    pdf_content = pdf.output(dest='S').encode('latin-1')
    pdf_bytes = BytesIO(pdf_content)

    return FileResponse(pdf_bytes, as_attachment=True, filename='notaPedido.pdf')

