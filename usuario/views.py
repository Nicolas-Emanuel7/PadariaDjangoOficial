import json
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth import logout as logout_django, login as login_django
from django.contrib.auth.decorators import login_required
from .models import Usuario
from gerenciamento.models import Avaliacao, EnderecoEntrega, Pedido, PedidoProduto, Produto, Avaliacao
import re
import datetime
from django.db import transaction

# FUNÇÕES DE LOGIN

def usuario_cadastro(request):
    if request.method == 'GET':
        usuarios_list = Usuario.objects.all()
        return render(request, 'usuario_cadastro.html', {'usuarios': usuarios_list})
    elif request.method == 'POST':
        username = request.POST.get('email')
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        telefone = request.POST.get('telefone')
        email = request.POST.get('email')
        password = request.POST.get('senha')
        cpf = request.POST.get('cpf')
        permissao = False

        user = Usuario.objects.filter(cpf=cpf)
        user = Usuario.objects.filter(email=email)

        if user.exists():
            return render(request, 'usuario_cadastro.html', {'nome': username, 'sobrenome':sobrenome, 'telefone': telefone, 'permissao': permissao, 'erro': 'Usuário já cadastrado!'})
        if not re.fullmatch(re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'), email):
            return render(request, 'usuario_cadastro.html', {'nome': username, 'sobrenome':sobrenome, 'telefone': telefone, 'cpf': cpf, 'permissao': permissao, 'erro': 'E-mail inválido!'})
        
        usuario = Usuario.objects.create(username=username, first_name=nome, last_name=sobrenome, cpf=cpf, telefone=telefone, email=email, password=password, permissao=permissao)
        print(username, nome, sobrenome, cpf, email, password, telefone, permissao)
        usuario.save()
        return render(request, 'usuario_cadastro.html')
    else:
        return render(request, 'usuario_cadastro.html')

@csrf_exempt
def usuario_login(request):
    if request.method == 'POST':
        usuarios_list = Usuario.objects.all()
        print(usuarios_list)
        emailInserido = request.POST.get('email')
        passwordInserida = request.POST.get('senha')

        for usuario in usuarios_list:
            if usuario.email == emailInserido and usuario.password == passwordInserida:
                login_django(request, usuario)
                # Usuário encontrado, autenticação bem-sucedida
                print('Usuário autenticado com sucesso!')
                # Faça qualquer ação adicional necessária
                if usuario.permissao == True:
                    return redirect('gerente_principal')
                else:
                    return redirect('usuario_principal')
        else:
            # Loop concluído sem encontrar um usuário correspondente
            print('Falha na autenticação!')

    return render(request, 'usuario_cadastro.html')

@login_required(login_url='/usuario/usuario_cadastro/')
def usuario_logout(request):
    # Exclui o pedido atual do usuário, se existir e não estiver completo
    if request.user.is_authenticated:
        pedido_incompleto = Pedido.objects.filter(cliente=request.user, completo=False).first()
        if pedido_incompleto:
            pedido_incompleto.delete()

    # Realiza o logout do usuário
    logout_django(request)
    
    # Redireciona para a página de login
    return redirect('usuario_cadastro')

# FUNÇÕES DA TELA PRINCIPAL

@login_required(login_url='/usuario/usuario_cadastro/')
def usuario_principal(request):
    produtos_list = Produto.objects.all()

    if request.user.is_authenticated:
        pedido, criado = Pedido.objects.get_or_create(cliente=request.user, data=datetime.datetime.now() , completo=False)
        itens = pedido.pedidoproduto_set.all()
        carrinho_itens = pedido.get_carrinho_itens
    else:
        itens = []
        carrinho_itens = {'get_carrinho_total': 0, 'get_carrinho_itens': 0}

    ingredientes_produto = {}
    for produto in produtos_list:
        ingredientes_produto[produto.id_produto] = produto.ingredientes.all()

    contexto = {'pedido':pedido ,'produtos': produtos_list, 'itens': itens, 'carrinho_itens': carrinho_itens, 'ingredientes_produto': ingredientes_produto}
    return render(request, 'usuario_principal.html', contexto)

@login_required(login_url='/usuario/cadastro/')
def usuario_produto(request, id_produto):
    produto = get_object_or_404(Produto, id_produto=id_produto)
    media_avaliacoes = Avaliacao.calcular_media_avaliacoes(produto)
    ingredientes_produto = produto.ingredientes.all()

    if request.user.is_authenticated:
        pedido, criado = Pedido.objects.get_or_create(cliente=request.user, data=datetime.datetime.now(), completo=False)
        itens = pedido.pedidoproduto_set.all()
        carrinho_itens = pedido.get_carrinho_itens
        avaliacoes = Avaliacao.objects.filter(produto=produto) 

        if request.method == 'POST':
            comentario = request.POST.get('comentario')
            nota = request.POST.get('nota')
            avaliacao = Avaliacao.objects.create(usuario=request.user, produto=produto, comentario=comentario, nota=nota)
            avaliacao.save()
            return redirect(f'/usuario/usuario_produto/{id_produto}/')
        
        else:
            avaliacoes = Avaliacao.objects.filter(produto=produto)
        
    else:
        itens = []
        carrinho_itens = {'get_carrinho_total': 0, 'get_carrinho_itens': 0}

    contexto = {'produto': produto, 'pedido': pedido, 'itens': itens, 'carrinho_itens': carrinho_itens, 'avaliacoes': avaliacoes, 'media_avaliacoes': media_avaliacoes, 'ingredientes_produto': ingredientes_produto}
    return render(request, 'usuario_produto.html', contexto)

@login_required(login_url='/usuario/usuario_cadastro/')
def usuario_pesquisa_produto(request):
    if request.user.is_authenticated:
        pedido, criado = Pedido.objects.get_or_create(cliente=request.user, data=datetime.datetime.now() , completo=False)
        itens = pedido.pedidoproduto_set.all()
        carrinho_itens = pedido.get_carrinho_itens
    else:
        itens = []
        carrinho_itens = {'get_carrinho_total': 0, 'get_carrinho_itens': 0}

    termo_pesquisa = request.GET.get('Pesquisar', '')
    resultados = Produto.objects.filter(nome_produto__icontains=termo_pesquisa)
    contexto = {'pedido':pedido , 'itens': itens, 'carrinho_itens': carrinho_itens, 'resultados': resultados, 'termo_pesquisa': termo_pesquisa}
    return render(request, 'usuario_pesquisa_produto.html', contexto)
        

# FUNÇÕES DO PERFIL

@login_required(login_url='/usuario/usuario_cadastro/')
def usuario_perfil(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('nome')
        user.last_name = request.POST.get('sobrenome')
        user.telefone = request.POST.get('telefone')
        user.endereco = request.POST.get('endereco')
        user.email = request.POST.get('email')
        user.password = (request.POST.get('senha'))
        user.username = (request.POST.get('nome'))
        user.save()
        return redirect('usuario_perfil')
    # Filtra os pedidos do usuário com valor maior que 0
    pedidos = Pedido.objects.filter(cliente=request.user, valor_final__gt=0)
    return render(request, 'usuario_perfil.html',{'pedidos': pedidos})

@login_required
def usuario_excluir_perfil(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        print('Usuário excluído com sucesso!')
        return render(request, 'usuario_cadastro.html')

# FUNÇÕES DO PEDIDO

@login_required(login_url='/usuario/usuario_cadastro/')
def usuario_carrinho(request):
    
    if request.user.is_authenticated:
        pedido, criado = Pedido.objects.get_or_create(cliente=request.user, data=datetime.datetime.now() , completo=False)
        itens = pedido.pedidoproduto_set.all()
        carrinho_itens = pedido.get_carrinho_itens
    else:
        itens = []
        carrinho_itens = {'get_carrinho_total': 0, 'get_carrinho_itens': 0}

    contexto = {'pedido':pedido , 'itens': itens, 'carrinho_itens': carrinho_itens}
    return render(request, 'usuario_carrinho.html', contexto)

@login_required(login_url='/usuario/usuario_cadastro/')
def usuario_checkout(request):
    
    if request.user.is_authenticated:
        pedido, criado = Pedido.objects.get_or_create(cliente=request.user, data=datetime.datetime.now() , completo=False)
        itens = pedido.pedidoproduto_set.all()
        carrinho_itens = pedido.get_carrinho_itens
    else:
        itens = []
        carrinho_itens = {'get_carrinho_total': 0, 'get_carrinho_itens': 0}

    contexto = {'pedido':pedido , 'itens': itens, 'carrinho_itens': carrinho_itens}
    return render(request, 'usuario_checkout.html', contexto)

@transaction.atomic
def update_item(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        id_produto = data['id_produto']
        action = data['action']

        print('Action:', action)
        print('Produto:', id_produto)

        cliente = request.user
        produto = Produto.objects.get(id_produto=id_produto)
        pedido, criado = Pedido.objects.get_or_create(cliente=cliente, completo=False)

        pedido_produto, criado = PedidoProduto.objects.get_or_create(pedido=pedido, produto=produto)

        if action == 'add':
            pedido_produto.quantidade_comprada = (pedido_produto.quantidade_comprada + 1)
        elif action == 'remove':
            pedido_produto.quantidade_comprada = (pedido_produto.quantidade_comprada - 1)
        
        pedido_produto.save()

        if pedido_produto.quantidade_comprada <= 0:
            pedido_produto.delete()

        return JsonResponse('Item adicionado', safe=False)

@csrf_exempt
def processa_pedido(request):
    id_transacao = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        cliente = request.user
        pedido, criado = Pedido.objects.get_or_create(cliente=cliente, completo=False)
        pedido.valor_final = float(data['form']['total'].replace(',', '.'))
        pedido.id_transacao = id_transacao

        if pedido.valor_final == pedido.get_carrinho_total:
            pedido.completo = True
        pedido.save()

        enderecoEntrega = EnderecoEntrega.objects.create(
            usuario=cliente,
            pedido=pedido,
            endereco=data['form']['endereco'],
            bairro=data['form']['bairro'],
            cidade=data['form']['cidade'],
            estado=data['form']['estado'],
        )
        enderecoEntrega.save()

    else:
        print('Usuário não está logado')

    return JsonResponse('Pedido processado', safe=False)







