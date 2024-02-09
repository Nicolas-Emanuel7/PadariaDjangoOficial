let sidebar = document.querySelector(".sidebar");
let closeBtn = document.querySelector("#btn");

closeBtn.addEventListener("click", ()=>{
    sidebar.classList.toggle("open");
    menuBtnChange();
});

function menuBtnChange() {
if(sidebar.classList.contains("open")){
    closeBtn.classList.replace("bx-menu", "bx-menu-alt-right");
}else {
    closeBtn.classList.replace("bx-menu-alt-right","bx-menu");
}
}



document.getElementById('logout-link').addEventListener('click', function(event) {
    event.preventDefault(); // Impede o comportamento padrão do link (redirecionamento)
        
    // Exibe um prompt de confirmação
    var confirmLogout = confirm('Tem certeza de que deseja sair?');

    // Se o usuário confirmar o logout, redireciona para a página de logout
    if (confirmLogout) {
        window.location.href = this.getAttribute('href');
    }
});

