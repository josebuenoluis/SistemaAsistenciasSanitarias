let estado=0;
let lampara = document.getElementById("lampara");
function llamada(){
    fetch('http://localhost/llamada/5/b').then(response => response.json());
    lampara.src = "/asistencias-sanitarias/static/img/pic_bulbon.gif";
    if(!lampara.classList.contains('encendido')){
        lampara.classList.add('encendido');
    }
}
function presencia(){
    let peticion = fetch('http://localhost/presencia/5/b').then(response => {
        return response.json()
    });
    peticion.then(respuesta => {
        if(respuesta.success == true){
            lampara.src = "/asistencias-sanitarias/static/img/pic_bulboff.gif";
            if(lampara.classList.contains('encendido')){
                lampara.classList.remove('encendido');
            }
        }
    });
}