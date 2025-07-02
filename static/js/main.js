const sidebar = document.querySelector(".sidebar");
const sidebarTogler = document.querySelector(".sidebar-toggler-header");
let desplegado = false;
sidebarTogler.addEventListener("click",() => {
    sidebar.classList.toggle("collapsed");
    if(desplegado == false){
        desplegado = true;
    }else{
        desplegado = false;
    }
    evaluarHeader();
});

window.addEventListener("resize", () => {
    evaluarHeader();
});

function evaluarHeader(){
    const header = document.querySelector(".header-content > header");
    const userIcon = header.querySelector(".icon-user");
    if(window.innerWidth <= 326 && desplegado == true){
        userIcon.style.display = "none";
    }else{
        setTimeout(() => {
            userIcon.style.display = "inline";
        }, 200);
    }
    actualizarContenido();
}

function actualizarContenido(){
    const content = document.querySelector("body main");
    if(desplegado == true){
        content.style.left = "270px";
    }else{
        content.style.left = "86px";
    }
}

