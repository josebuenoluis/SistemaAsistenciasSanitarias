


function generarCodigoAsistente() {
    let input = document.getElementById("codigo");
    const caracteres = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    let codigo = '';
    for (let i = 0; i < 6; i++) {
        const indiceAleatorio = Math.floor(Math.random() * caracteres.length);
        codigo += caracteres[indiceAleatorio];
    }
    input.value = codigo;
}

function validarTelefono(){
    let input = document.getElementById("telefono");
    let telefono = input.value;
    let valido = false;
    if(telefono.length == 9 && !isNaN(telefono)){
        valido = true;
    }else{
        valido = false;
    }
    if(valido == false){
        if(!input.classList.contains("is-invalid")){
            input.classList.add("is-invalid");
        };
    }else{
        if(input.classList.contains("is-invalid")){
            input.classList.remove("is-invalid");
        };
        if(!input.classList.contains("is-valid")){
            input.classList.add("is-valid");
        }
    }
}

function validarNif(nif=""){
    let input = document.getElementById("nif");
    nif = nif == "" ? input.value.toUpperCase() : nif;
    let letras = "TRWAGMYFPDXBNJZSQVHLCKE";
    let valido = false;
    let nifNumeros = nif.substring(0,8);
    if(nif.length == 9 || letras.includes(nif.at(-1))){
        valido = false;
        if(nifNumeros.at(0) == "X"){
            nifNumeros = "0" + nifNumeros.substring(1,8);
        }else if(nifNumeros.at(0) == "Y"){
            nifNumeros = "1" + nifNumeros.substring(1,8);
        }else if(nifNumeros.at(0) == "Z"){
            nifNumeros = "2" + nifNumeros.substring(1,8);
        }
        if(!isNaN(nifNumeros)){
            let letra = letras.charAt(nifNumeros % 23);
            if(letra == nif.at(-1)){
                valido = true;
            }else{
                valido = false;
            }
        }else{
            valido = false;
        }
    }
    if(valido == false){
        if(!input.classList.contains("is-invalid")){
            input.classList.add("is-invalid");
        };
    }else{
        if(input.classList.contains("is-invalid")){
            input.classList.remove("is-invalid");
        };
        if(!input.classList.contains("is-valid")){
            input.classList.add("is-valid");
        }
    }
    return valido;
}

function getData(e){
    e.preventDefault();
    let formulario = document.getElementById("form-crear-asistente");
    if(formulario.checkValidity()){   
        let formData = new FormData(formulario);
        let dataAsistente = {
            nif: formData.get("nif").toUpperCase(),
            nombre: formData.get("nombre"),
            telefono: formData.get("telefono"),
            codigo: formData.get("codigo"),
            planta: formData.get("planta")
        };
        let mensajesValidaciones = validarCampos(dataAsistente);
        if(mensajesValidaciones.length == 0){
            postAsistente(dataAsistente).then(data => {
                abrirModal(data);
            });
        }else{
            abrirModal({"success":false,"message":mensajesValidaciones});
        }

    }else{
        formulario.reportValidity();
    }
}

function validarCampos(dataAsistente){
    let mensajes = [];
    if(validarNif(dataAsistente.nif) == false){
        mensajes.push("El DNI/NIE ingresado no es válido.");
    }
    if(isNaN(dataAsistente.telefono) || dataAsistente.telefono.length != 9) {
        mensajes.push("El teléfono ingresado no es válido.");
    }
    if(dataAsistente.codigo.length != 6){
        mensajes.push("El código de asistente ingresado no es válido.");
    }
    return mensajes;
}

async function postAsistente(data){
    let url = "/asistentes/crear";
    return await fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    }).then(data => {
        return data.json();
    }).catch(error => {
        console.error("Error:", error);
    });

}

function abrirModal(respuestaServidor){
    let modal = document.getElementById("modal-mensajes");
    let fade = document.createElement("div");
    let modalBody = document.getElementById("modal-body");
    let btnCerrar = document.getElementById("btn-cerrar");
    let formulario = document.getElementById("form-crear-asistente");
    fade.classList.add("modal-backdrop");
    fade.classList.add("fade");
    fade.classList.add("show");
    fade.style.zIndex = "1050";
    setTimeout(() => {
        fade.classList.add("in");
        modal.classList.add("in");
    }, 10);
    document.body.appendChild(fade);
    modal.classList.add("fade");
    modal.classList.add("show");
    modal.setAttribute("style","display: block;");
    modal.style.zIndex = "1055";
    btnCerrar.focus();
    document.body.classList.add("modal-open");
    if(respuestaServidor.success == true){
        modalBody.innerHTML = `<div class="alert alert-success" role="alert">
        ${respuestaServidor.message[0]}
        </div>`;
        formulario.reset();
    }else{
        for(let i = 0; i < respuestaServidor.message.length; i++){
            modalBody.innerHTML += `<div class="alert alert-danger" role="alert">
            ${respuestaServidor.message[i]}
            </div>`;
        }
    }
}

function cerrarModal(){
    let modal = document.getElementById("modal-mensajes");
    let fade = document.querySelector(".modal-backdrop");
    let modalBody = document.getElementById("modal-body");
    modal.classList.remove("show");
    modal.setAttribute("style","display: none;");
    modalBody.innerHTML = "";
    document.body.classList.remove("modal-open");
    fade.remove();
}
