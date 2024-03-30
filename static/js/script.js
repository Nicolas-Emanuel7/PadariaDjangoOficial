function addIngrediente() {
    var container = document.getElementById("form-ingrediente");
    
    var html = "<div class='row'>";
    html += "<div class='col-md'>";
    html += "<input type='text' class='ingrediente-entrada' name='nome_ingrediente' placeholder='Nome do ingrediente'>";
    html += "</div>";
    html += "<div class='col-md'>";
    html += "<input type='text' class='ingrediente-entrada'  name='unidade_Medida' placeholder='Unidade de medida' >";
    html += "</div>";
    html += "<div class='col-md'>";
    html += "<button type='button' onclick='removerIngrediente(this)' class='btn btn-danger'>Excluir</button>";
    html += "</div>";
    html += "</div>";
    console.log("mais um ingrediente")

    container.innerHTML += html;
} //faz



function removerIngrediente(button) {
    // Obtém o elemento pai do botão (a div 'row' que contém o input e o botão)
    var row = button.parentNode.parentNode;
    // Remove o elemento pai (a linha inteira) do container
    row.parentNode.removeChild(row);
}

function exibir_produto(tipo){
    
    var add_produto = document.getElementById("add-produto");
    var att_produto = document.getElementById("att-produto");

    if(tipo == '1'){
        
        add_produto.style.display = "block";
        att_produto.style.display = "none";
        console.log("ADD produto")
    }else if(tipo == '2'){
        console.log("ATT produto")
        add_produto.style.display = "none";
        att_produto.style.display = "block";
    }
}

function exibir_funcionario(tipo){
    
    var add_funcionario = document.getElementById("add-funcionario");
    var att_funcionario = document.getElementById("att-funcionario");

    if(tipo == '1'){
        
        add_funcionario.style.display = "block";
        att_funcionario.style.display = "none";
        console.log("ADD funcionario")
    }else if(tipo == '2'){
        console.log("ATT funcionario")
        add_funcionario.style.display = "none";
        att_funcionario.style.display = "block";
    }
}

function update_funcionario(){
    id = document.getElementById("id_funcionario").value;
    console.log(id)
    nome_funcionario = document.getElementById("nome_funcionario").value;
    console.log(nome_funcionario)
    telefone_funcionario = document.getElementById("telefone_funcionario").value;
    console.log(telefone_funcionario)
    cargo = document.getElementById("cargo").value;
    console.log(cargo)
    salario = document.getElementById("salario").value;
    console.log(salario)

    fetch('/gerenciamento/gerente_att_funcionario/' + id, {
        method: "POST",
        headers: {
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            nome_funcionario: nome_funcionario,
            telefone_funcionario: telefone_funcionario,
            cargo: cargo,
            salario: salario,
        })
    }).then(function (result){
        return result.json()
    }).then (function(data){
        console.log(data)
        nome_funcionario = data['nome_funcionario'];
        telefone_funcionario = data['telefone_funcionario'];
        cargo = data['cargo'];
        salario = data['salario'];
        console.log('Sucesso')
    })
}

function dados_funcionario() {
    funcionario = document.getElementById('funcionario-select')
    csrf_token = document.querySelector('[name=csrfmiddlewaretoken]').value;
    id_funcionario = funcionario.value;
    console.log(id_funcionario)

    data =  new FormData();
    data.append('id_funcionario', id_funcionario);

    fetch('/gerenciamento/dados_funcionario/', {
        method: "POST",
        headers: {
            'X-CSRFToken': csrf_token,
        },
        body: data
    }).then(function(result){
        return result.json()
    }).then(function(data){
        console.log(data)
        document.getElementById('form-att-funcionario').style.display = 'block'

        id_funcionario = document.getElementById('id_funcionario')
        id_funcionario.value = data['id_funcionario']

        nome_funcionario = document.getElementById('nome_funcionario')
        nome_funcionario.value = data['nome_funcionario']

        telefone_funcionario = document.getElementById('telefone_funcionario')
        telefone_funcionario.value = data['telefone_funcionario']

        cargo = document.getElementById('cargo')
        cargo.value = data['cargo']
        console.log(data['cargo'])

        salario = document.getElementById('salario')
        salario.value = data['salario']
        console.log(data['salario'])

    })
    .catch(error => console.error('Erro ao buscar dados do funcionário:', error));
}

function dados_produto(id_produto){
    var att_produto = document.getElementById("att-produto");
    att_produto.style.display = "block";
    console.log(id_produto)
    csrf_token = document.querySelector('[name=csrfmiddlewaretoken]').value;
    data =  new FormData();
    data.append('id_produto', id_produto);
    fetch("/gerenciamento/dados_produto/",{
        method: "POST",
        headers: {
            'X-CSRFToken': csrf_token,
        },
        body: data
    }).then(function(result){
        return result.json()
    }).then(function(data){
        console.log(data)
        document.getElementById('att-produto').style.display = 'block'

         // Limpar o conteúdo atual dos ingredientes
        var div_ingredientes = document.getElementById('form-ingrediente');
        div_ingredientes.innerHTML = '';

        for(i=0; i<data['ingredientes'].length; i++){
            div_ingredientes.innerHTML += 
            "<div class='row'>\
                <div class='col-md'>\
                    <input type='text' class='ingrediente-entrada' name='nome_ingrediente' value='"+ data['ingredientes'][i]['nome_ingrediente'] + "'>\
                </div>\
                <div class='col-md'>\
                    <input type='text' class='ingrediente-entrada'  name='unidade_Medida'  value='"+ data['ingredientes'][i]['unidade_Medida'] + "'>\
                </div>\
                <div class='col-md'>\
                    <a href='/gerenciamento/excluir_ingrediente/"+ data['ingredientes'][i]['id_ingrediente'] + '/' + data['id_produto'] + "' class='btn btn-danger'>Excluir</a>\
                </div>\
            </div><br>"
        }
    })
}

function cancelarAtualizacao() {
    document.getElementById('att-produto').style.display = 'none';
}

function substituirVirgulaPorPonto() {
    var precoInput = document.getElementsByName('preco')[0];
    precoInput.value = precoInput.value.replace(',', '.');
}

// PRINCIPAL

var updateBtns = document.getElementsByClassName('update-cart')

for(var i = 0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){
        var id_produto = this.dataset.produto
        var action = this.dataset.action
        console.log('id_produto:', id_produto, 'Action:', action)

        console.log('USER:', user)
        if(user === 'AnonymousUser'){
            console.log('Não logado')
        }
        else{
            updateUserOrder(id_produto, action)
        }
    })
}

function updateUserOrder(id_produto, action){
    console.log('Logado, enviando dados...')

    var url = '/usuario/usuario_update_item/'

    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken': csrftoken,
        },
        body:JSON.stringify({'id_produto':id_produto, 'action':action})
    })

    .then((response) =>{
        return response.json()
    })
    .then((data) =>{
        console.log('data:', data)
        location.reload()
    })
}

function exibir_perfil(tipo){

    att_perfil = document.getElementById('att-perfil');
    mostrar_pedidos = document.getElementById('mostrar-pedidos');

    if(tipo == 1){
        att_perfil.style.display = 'none';
        mostrar_pedidos.style.display = 'block';
    }else if(tipo == 2){
        att_perfil.style.display = 'none';
        mostrar_pedidos.style.display = 'block';
    }
}

var updateBtns = document.querySelectorAll('.update-cart');

updateBtns.forEach(function(btn) {
    btn.addEventListener('click', function() {
        var id_produto = this.dataset.produto;
        var action = this.dataset.action;
        console.log('id_produto:', id_produto, 'Action:', action);
        
        if (user === 'AnonymousUser') {
            console.log('Usuário não logado');
        } else {
            console.log('Logado')
            updateUserOrder(id_produto, action);
        }
    });
});

function updateUserOrder(id_produto, action) {
    console.log('Enviando dados...');
    var url = '/usuario/usuario_update_item/';

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({ 'id_produto': id_produto, 'action': action })
    })
    .then(function(response) {
        return response.json();
    })
    .then(function(data) {
        console.log('Data:', data);
        location.reload(); // Recarrega a página após a atualização do item no carrinho
    })
    .catch(function(error) {
        console.error('Erro:', error);
    });
}

// Função para mostrar o modal de confirmação
function confirmarExclusao(produtoId) {
    var modal = document.getElementById('modal-confirmacao');
    modal.style.display = 'block';
    // Guarde o ID do produto a ser excluído em uma variável global para acessá-lo depois
    window.produtoIdParaExcluir = produtoId;
}

// Função para fechar o modal de confirmação
function fecharModal() {
    var modal = document.getElementById('modal-confirmacao');
    modal.style.display = 'none';
}

// Função para excluir o produto
function excluirProduto(produtoId) {
    // Aqui você pode enviar uma requisição AJAX para excluir o produto
    // Certifique-se de incluir o CSRF token na requisição
    var csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    fetch('/gerenciamento/gerente_excluir_produto/' + produtoId, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ produto_id: produtoId })
    })
    .then(response => {
        if (response.ok) {
            alert('Produto excluído com sucesso');
            // Atualizar a página ou fazer outras ações necessárias após excluir o produto
        } else {
            alert('Erro ao excluir o produto');
        }
    })
    .catch(error => {
        console.error('Erro ao excluir o produto:', error);
        alert('Erro ao excluir o produto');
    })
    .finally(() => {
        // Fechar o modal de confirmação após excluir o produto
        fecharModal();
    });
}



function confirmarExclusao() {
    if (window.confirm("Tem certeza de que deseja excluir o perfil?")) {
        excluirPerfil();
    } else {
        // Código a ser executado se o usuário cancelar a exclusão
        console.log("Exclusão cancelada pelo usuário.");
    }
}

function excluirPerfil() {
    fetch('/gerenciamento/excluir_perfil/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({})
    })
    .then(response => {
        if (response.ok) {
            alert("Perfil excluído com sucesso!");
            window.location.href = '/usuario/cadastro/';
        } else {
            alert("Ocorreu um erro ao excluir o perfil.");
        }
    })
    .catch(error => console.error('Erro ao excluir o perfil:', error));
}