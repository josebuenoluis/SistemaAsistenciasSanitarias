let tabla = document.getElementById("tabla-asistencias");
let nombreArchivo = "";
function obtenerAsistencias(){
    let data = [];
    let datosArchivo = {};
    let tbody = tabla.querySelector("tbody");
    let theaders = tabla.querySelector("thead");
    let delimitador = document.getElementById("delimitador").value;
    let correo = document.getElementById("correo").value;
    let nombre = document.getElementById("nombre-archivo").value;
    if(nombre != ""){
        nombreArchivo = nombre + ".csv";
    }
    datosArchivo["delimitador"] = delimitador != "" ? delimitador : ",";
    datosArchivo["correo"] = correo;
    datosArchivo["nombre"] = nombreArchivo;
    data.push(datosArchivo);

    for(let row = 0; row < tbody.rows.length;row++){
        let childRow = tbody.rows[row];
        let object = {};
        for(let cell = 0; cell < childRow.cells.length;cell++){
            let header = theaders.rows[0].cells[cell].textContent;
            object[header] = childRow.cells[cell].textContent;
        }
        data.push(object);
    }
    if(data.length > 0){
        postData(data).then(response =>{
            
        });
    }
}

function limpiarFiltros(){
    let modalFiltros = document.getElementById("exampleModal");
    let filtrosInput = modalFiltros.querySelectorAll("input,select");

}

function limpiarTabla(){
    let tabla = document.querySelector("table");
    let tbody = tabla.querySelector("tbody");
    for(let row = 1; row < tbody.rows.length; row++){
        tbody.deleteRow(row);
    }
    for(let i = tbody.rows.length - 1; i >= 0; i--) {
        tbody.deleteRow(i);
    }
}

function mostrarAsistencias(data){
    let tabla = document.querySelector("table");
    let tbody = tabla.querySelector("tbody");
    data.forEach(element => {
        let fila = document.createElement("tr");
        let celdaId = document.createElement("td");
        celdaId.textContent = element.id;
        fila.appendChild(celdaId);
        let celdaNif = document.createElement("td");
        celdaNif.textContent = element.asistente_fk;
        fila.appendChild(celdaNif);
        let celdaHabitacion = document.createElement("td");
        celdaHabitacion.textContent = element.habitacion_fk;
        fila.appendChild(celdaHabitacion);
        let celdaCama = document.createElement("td");
        celdaCama.textContent = element.cama_fk;
        fila.appendChild(celdaCama);
        let celdaLlamada = document.createElement("td");
        celdaLlamada.textContent = element.fecha_llamada;
        fila.appendChild(celdaLlamada);
        let celdaPresencia = document.createElement("td");
        celdaPresencia.textContent = element.fecha_presencia;
        fila.appendChild(celdaPresencia);
        let celdaEstado = document.createElement("td");
        celdaEstado.textContent = element.estado.charAt(0).toUpperCase() + element.estado.slice(1,element.estado.length) ;
        fila.appendChild(celdaEstado);
        tbody.appendChild(fila);
    })
}

function obtenerFiltros(){
    let modalFiltros = document.getElementById("exampleModal");
    let filtrosInput = modalFiltros.querySelectorAll("form input,select");
    // Obtenemos todos los campos del modal de filtros
    let datos = {};
    let fechas = {};
    filtrosInput.forEach(element => {
        console.log(element);
        if(element.id == "desde" || element.id == "hasta"){
            if(element.value != ""){
                fechas[element.id] = element.value;
                datos["fechas"] = fechas;
            }
        }else if(element.value != ""){
            datos[element.id] = element.value;
        }
    });
    console.log(datos);
    obtenerAsistenciasFiltros(datos).then(data => {
        limpiarTabla();
        mostrarAsistencias(data);
    });
}

async function obtenerAsistenciasFiltros(data){
    let endpoint = "/api/asistencias/exportar/filtros"
    return await fetch(endpoint,{
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify(data)
    }).then(response => {
        return response.json();
    }).catch(error =>{
        console.log("Error: ",error);
    });
}


async function postData(data){
    let endpoint = "/asistencias/exportar"; 
    return await fetch(endpoint,{
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify(data)
    }).then(response =>{
        response.blob().then(blob =>{
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = nombreArchivo != "" ? nombreArchivo : "asistencias.csv";
            document.body.appendChild(a);
            a.click(); 
            a.remove();
            window.URL.revokeObjectURL(url);
        });
    }).catch(error =>{
        console.log("Error: ",error);
    });
}

