let habitacionOption = document.getElementById("habitacion");
let rowsSelectedDocument = [];
let modeUpdate = false;
let rowsUpdateValues = [];
let plantas = [];
let habitaciones = [];
let camas = [];

obtenerHabitaciones().then(data => {
    habitaciones = data;
});

obtenerCamasHabitaciones().then(data => {
    camas = data;
});

async function obtenerHabitaciones(){
    let endpoint = "/api/habitaciones";
    return await fetch(endpoint,{
        method:"GET",
        headers:{
            "Content-Type":"application/json"
        }
    }).then(data => {
        return data.json();
    }).catch(error =>{
        console.log("Error al obtener habitaciones: ",error);
    });
}

async function obtenerCamasHabitaciones(){
    let endpoint = `/api/asistencias/dispositivos/camas`;
    return await fetch(endpoint,{
        method:"GET",
        headers:{
            "Content-Type":"application/json"
        }
    }).then(data => {
        return data.json();
    }).catch(error =>{
        console.log("Error al obtener camas: ",error);
    });
}

async function obtenerCamasHabitacion(n_habitacion){
    let endpoint = `/api/asistencias/dispositivos/camas?numerohabitacion=${n_habitacion}`;
    return await fetch(endpoint,{
        method:"GET",
        headers:{
            "Content-Type":"application/json"
        }
    }).then(data => {
        return data.json();
    }).catch(error =>{
        console.log("Error al obtener camas: ",error);
    });
}

function reiniciar(){
    let camaOption = document.getElementById("cama");
    while (camaOption.options.length > 1) {
        camaOption.remove(1);
    }
    camaOption.disabled = true;
}

function mostrarCamasHabitacion(){
    let camaOption = document.getElementById("cama");
    if(habitacionOption.value != ""){
        obtenerCamasHabitacion(habitacionOption.value).then(data => {
            while (camaOption.options.length > 1) {
                camaOption.remove(1);
            }
            data.forEach(element => {
                let option = document.createElement("option");
                option.value = element.id;
                option.textContent = "Cama " + element.nombre.toUpperCase();
                camaOption.appendChild(option);
            });
            if(camaOption.disabled) {
                camaOption.disabled = false;
            }
        });
    }else{
        camaOption.disabled = true;
    }
}

function seleccionarAsistente(event) {
    let rowSelect = event.target.closest('tr');
    for (let cell = 0; cell < rowSelect.cells.length; cell++) {
      if (rowSelect.cells[cell].style.background != 'rgb(170, 190, 192)') {
        rowSelect.cells[cell].style.background = 'rgb(170, 190, 192)';
        if (rowsSelectedDocument.indexOf(rowSelect.rowIndex) == -1) {
          rowsSelectedDocument.push(rowSelect.rowIndex);
        }
      }else{
        rowSelect.cells[cell].style.background = '';
        if (rowsSelectedDocument.indexOf(rowSelect.rowIndex) != -1) {
          let positionRowSelect = rowsSelectedDocument.indexOf(
            rowSelect.rowIndex
          );
          rowsSelectedDocument.splice(positionRowSelect, 1);
        }
      }
    }
    contarSeleccionados();
  }

function buscarAsistentes(){
    let table = document.querySelector("table");
    let tbody = table.querySelector('tbody');
    let input = document.getElementById("buscar-asistentes");
    if(tbody){
        let rows = tbody.rows;
        for (let row = 0; row < rows.length; row++) {
        let rowTable = rows[row];
        let refRowTable = rowTable.cells[2].textContent?.toLowerCase() || '';
        if (!refRowTable.includes(input.value.toLowerCase())) {
            rowTable.style.display = 'none';
        } else {
            rowTable.style.display = '';
        }
        }
    }
}

function filtrarPlanta(){
    let table = document.querySelector("table");
    let tbody = table.querySelector('tbody');
    let input = document.getElementById("planta");
    if(tbody){
      let rows = tbody.rows;
      for (let row = 0; row < rows.length; row++) {
        let rowTable = rows[row];
        let refRowTable = rowTable.cells[4].textContent?.toLowerCase() || '';
        if (!refRowTable.includes(input.value.toLowerCase())) {
          rowTable.style.display = 'none';
        } else {
          rowTable.style.display = '';
        }
      }
    }
}

function contarSeleccionados(){
    let nItems = document.getElementById("n-items");
    nItems.textContent = rowsSelectedDocument.length.toString();
    let btnDelete = document.getElementById("btn-delete");
    if(rowsSelectedDocument.length > 0 && modeUpdate == false){
      if (!btnDelete.hasAttribute("data-bs-toggle")) {
        btnDelete.setAttribute("data-bs-toggle", "modal");
      }
      if (!btnDelete.hasAttribute("data-bs-target")) {
        btnDelete.setAttribute("data-bs-target", "#modalConfirm");
        btnDelete.onclick = () => {};
      }
    }else if(rowsSelectedDocument.length > 0 && modeUpdate == true){
      btnDelete.removeAttribute("data-bs-toggle");
      btnDelete.removeAttribute("data-bs-target");
      btnDelete.onclick = () => saveUpdate();
    }else if(rowsSelectedDocument.length == 0){
      btnDelete.removeAttribute("data-bs-toggle");
      btnDelete.removeAttribute("data-bs-target");
      btnDelete.onclick = () => {};
    }
  }

function actualizarAsistentes(){
    let table = document.querySelector("table");
    let tbody = table?.querySelector("tbody");
    let headers = table?.querySelectorAll("thead th");
    // Iteramos en los seleccionados para cambiar sus campos por inputs
    // editables.
    let values = []
    if(rowsSelectedDocument.length && modeUpdate == false){
      if(tbody && headers){
          for(let rowIndex of rowsSelectedDocument){
            let rowSelect = tbody.rows[rowIndex-1];
            let dataRow = {};
            for(let cell = 0; cell < rowSelect.cells.length;cell++){
              let header = headers[cell].textContent;
              if(header){
                let valueCell = rowSelect.cells[cell].textContent;
                dataRow[header] = valueCell;
              }
            }
            dataRow["index"] = rowIndex;
            values.push(dataRow);
          }
        rowsUpdateValues = values;
        // Comenzamos a convertir sus campos en inputs editables
          for(let rowIndex of rowsSelectedDocument){
            let rowSelect = tbody.rows[rowIndex-1];
            rowSelect.onclick = () => {};
            for(let cell = 0; cell < rowSelect.cells.length;cell++){
              let header = headers[cell].textContent;
              let cellSelect = rowSelect.cells[cell];
              let includeInput = cellSelect.firstElementChild;
              if(includeInput==null){
                cellSelect.textContent = "";
                let selectOptions = document.createElement("select");
                selectOptions.className ="form-select";
              if(header=="Habitacion"){
                let valorHabitacion = values.find(element => element.index == rowIndex)["Habitacion"];
                habitaciones.forEach(habitacion => {
                  let option = document.createElement("option");
                  option.value = habitacion.numero;
                  option.textContent = habitacion.numero;
                  selectOptions.appendChild(option);
                })
                selectOptions.value = valorHabitacion;
                selectOptions.onchange = (event) => mostrarCamasHabitacionesActualizar(event);
                cellSelect.appendChild(selectOptions);
              }else if(header=="Cama"){ 
                let rowValue = values.find(element => element.index == rowIndex);
                let valorCama = values.find(element => element.index == rowIndex)["Habitacion"];
                let camaId = camas.find(element => element.habitacion_fk.toString() == valorCama && element.nombre.toLowerCase()).id;
                camas.forEach(cama => {
                  if(cama.habitacion_fk.toString() == rowValue["Habitacion"]){
                      let option = document.createElement("option");
                      option.value = cama.id;
                      option.textContent = "Cama "+cama.nombre.toUpperCase();
                      selectOptions.appendChild(option);
                    }  
                })
                selectOptions.value = camaId.toString();
                cellSelect.appendChild(selectOptions);
            }
              else{
                let input = document.createElement("input");
                input.type = "text";
                input.className = "form-control text-center";
                cellSelect.appendChild(input);
                values.forEach(element => {
                  if(element.index == rowIndex){
                    if(header == "Id"){
                      input.value = element["Id"];
                      input.readOnly = true;
                    }else if(header == "Tipo"){
                      input.value = element["Tipo"];
                    }else if(header == "Ip"){
                      input.value = element["Ip"];
                    }else if(header == "Puerto"){
                      input.value = element["Puerto"];
                      input.maxLength = 65536;
                    }else if(header == "Fecha registro"){
                      input.value = element["Fecha registro"];
                      input.readOnly = true;
                    }
                  }
                })
              }
            }
          }
        }
      }
    }
    switchUpdate();
  }

function mostrarCamasHabitacionesActualizar(event){
    let selectEvent = event.target;
    let rowSelect = selectEvent.closest("tr");
    let habitacion = selectEvent.value;
    let camasHabitacion = [];
    for(let camaIndex = 0; camaIndex < camas.length; camaIndex++){
        let cama = camas[camaIndex];
        if(cama.habitacion_fk.toString() == habitacion){
            camasHabitacion.push(cama);
        }
    }
    let selectOption = rowSelect.cells[5].querySelector('select');
    if (selectOption) {
        while (selectOption.options.length > 0) {
            selectOption.remove(0);
        }
    }
    for(let camaIndex = 0; camaIndex < camasHabitacion.length; camaIndex++){
        let cama = camasHabitacion[camaIndex];
        let option = document.createElement("option");
        option.value = cama.id;
        option.textContent = "Cama "+cama.nombre.toUpperCase();
        selectOption.appendChild(option);
    }
}

  function switchUpdate(){
    let table = document.querySelector("table");
    let tbody = table?.querySelector("tbody");
    let includesInput = tbody?.querySelectorAll("input");
    let btnDelete = document.getElementById("btn-delete");
    let btnIcon = btnDelete?.firstElementChild;
    if(includesInput){
      let inputInclude = includesInput[0];
      if(inputInclude == undefined){
        modeUpdate = false;
        if(btnIcon){
          if(btnIcon.className == "bi bi-check-circle-fill text-success fs-1"){
            btnIcon.className = "bi bi-trash text-danger fs-1";
          }
        }
      }else{
        modeUpdate = true;
        if(btnIcon){
          if(btnIcon.className == "bi bi-trash text-danger fs-1"){
            btnIcon.className = "bi bi-check-circle-fill text-success fs-1";
            contarSeleccionados();
          }
        }
      }
    }
  }

function limpiarSeleccion() {
  let table = document.querySelector("table");
  let tbody = table.querySelector("tbody");
  let selectedRows = rowsSelectedDocument.sort((rowA, rowB) => rowB - rowA);
  if (tbody) {
    for (let rowIndex of selectedRows) {
      let rowSelect = tbody.rows[rowIndex - 1];
      rowSelect.onclick = (event) => seleccionarAsistente(event);
      for (let cell = 0; cell < rowSelect.cells.length; cell++) {
        if (rowSelect.cells[cell].style.background == 'rgb(170, 190, 192)') {
          rowSelect.cells[cell].style.background = "";
        }
      }
      // Obtenemos los valores de las celdas en el update si las hay
      // para eliminar inputs de edicion y reasignar textContent con sus valores,
      // mediante el atributo index debemos asegurarnos que estamos asignando la
      // row indicada
      if (rowsUpdateValues.length > 0) {
        let table = document.querySelector("table");
        let headers = table?.querySelectorAll("thead th");
        if (headers) {
          rowsUpdateValues.forEach(element => {
            if (element.index == rowSelect.rowIndex) {
              for (let cell = 0; cell < rowSelect.cells.length; cell++) {
                let header = headers[cell].textContent;
                let cellUpdate = rowSelect.cells[cell];
                let childCell = cellUpdate.firstElementChild;
                if (childCell) {
                  cellUpdate.removeChild(childCell);
                  if (header) {
                    cellUpdate.textContent = element[header];
                  }
                }
              }
            }
          })
        }
      }
    }
  }
  rowsSelectedDocument = [];
  contarSeleccionados();
  switchUpdate();
}

async function saveUpdate(){
    let table = document.querySelector("table");
    let tbody = table.querySelector("tbody");
    let btnDelete = document.getElementById("btn-delete");
    let rowsUpdate = [];
    if(tbody){
      for(let rowIndex of rowsSelectedDocument){
        let rowSelect = tbody.rows[rowIndex-1];
        let id = rowSelect.cells[0].querySelector('input') 
        ? rowSelect.cells[0].querySelector('input')?.value 
        : rowSelect.cells[0].textContent;
        let tipo = rowSelect.cells[1].querySelector('input') 
        ? rowSelect.cells[1].querySelector('input')?.value 
        : rowSelect.cells[1].textContent;
        let ip = rowSelect.cells[2].querySelector('input') 
        ? rowSelect.cells[2].querySelector('input')?.value 
        : rowSelect.cells[2].textContent;
        let puerto = rowSelect.cells[3].querySelector('input') 
        ? rowSelect.cells[3].querySelector('input')?.value 
        : rowSelect.cells[3].textContent;
        let habitacion = rowSelect.cells[4].querySelector('select') 
        ? rowSelect.cells[4].querySelector('select')?.value 
        : rowSelect.cells[4].textContent;
        let cama = rowSelect.cells[5].querySelector('select') 
        ? rowSelect.cells[5].querySelector('select')?.value 
        : rowSelect.cells[5].textContent;
        let dispositivo = {
            "id":id,
            "tipo":tipo,
            "ip":ip,
            "puerto":puerto,
            "habitacion":habitacion,
            "cama":cama,
        }
        rowsUpdate.push(dispositivo);
      }
      let respuestaServidor = "";
      updateResponse(rowsUpdate).then(respuesta => {
        respuestaServidor = respuesta;
      });
      // Luego de actualizar los elementos, mostramos nuevamente la tabla
      // con los elementos actualizados.
      clearTable();
      rowsSelectedDocument = [];
      contarSeleccionados();
      let loading = document.createElement("div");
      loading.className = "loading d-flex justify-content-center align-items-center";
      loading.id = "loading";
      loading.style.marginTop = "100px";
      let loadingIcon = document.createElement("i");
      loadingIcon.className = "bi bi-arrow-clockwise text-success fs-1";
      loadingIcon.style.animation = "spin 2s linear infinite";
      const style = document.createElement("style");
      style.textContent = `
      @keyframes spin {
        from {
          transform: rotate(0deg);
          }
        to {
          transform: rotate(360deg);
          }
        }
      `;
      document.head.appendChild(style);
      loading.appendChild(loadingIcon);
      let tableContainter = document.querySelector(".table-responsive");
      tableContainter.appendChild(loading);
      new Promise(resolve => setTimeout(resolve, 3000)).then(() => {
        mostrarAsistentes();
        let container = document.querySelector(".loading");
        if(container){
          tableContainter.removeChild(container);
          switchUpdate();
          btnDelete.onclick = () => {};
        }
        abrirModal(respuestaServidor);
      });
    }
}

async function mostrarAsistentes(){
    let table = document.querySelector("table");
    let tbody = table.querySelector("tbody");
    clearTable();
    obtenerDispositivos().then(data => {
      data.forEach(element => {
        let newRow = document.createElement("tr");
        newRow.onclick = (event) => seleccionarAsistente(event);
        let cellId = document.createElement("td");
        cellId.textContent = element.id;
        newRow.appendChild(cellId);
        let cellTipo = document.createElement("td");
        cellTipo.textContent = element.tipo;
        newRow.appendChild(cellTipo);
        let cellIp = document.createElement("td");
        cellIp.textContent = element.ip;
        newRow.appendChild(cellIp);
        let cellPuerto = document.createElement("td");
        cellPuerto.textContent = element.puerto;
        newRow.appendChild(cellPuerto);
        let cellHabitacion = document.createElement("td");
        cellHabitacion.textContent = element.habitacion_fk;
        newRow.appendChild(cellHabitacion);
        let cellCama = document.createElement("td");
        cellCama.textContent = element.nombre_cama;
        newRow.appendChild(cellCama);
        let cellFecha = document.createElement("td");
        cellFecha.textContent = element.fecha_registro;
        newRow.appendChild(cellFecha);
        tbody?.appendChild(newRow);
      })
    })
  }
  
async function obtenerDispositivos(){
    return await fetch("/api/dispositivos",{
        method:"GET",
        headers:{
            "Content-Type":"application/json"
        },
    }).then(response => {
        if(response.ok){
            return response.json();
        }else{
            console.error("Error al obtener los dispositivos");
        }
    }).catch(error => {
        console.log("Error: ",error);
    })
}

async function updateResponse(dataDispostivos) {
  return await fetch("/asistencias/dispositivos", {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(dataDispostivos),
  })
    .then((response) => {
      if (response.ok) {
        return response.json();
      } else {
        console.log("Error al actualizar");
      }
    })
    .catch((error) => {
      console.log(error);
    });
}

function clearTable(){
    let table = document.querySelector("table");
    let tbody = table.querySelector("tbody");
    if (tbody) {
      while (tbody.firstChild) {
        tbody.removeChild(tbody.firstChild);
      }
    }
}

async function eliminarDispositivosResponse(ids){
    return await fetch("/asistencias/dispositivos",{
        method:"DELETE",
        headers:{
            "Content-Type":"application/json"
        },
        body: JSON.stringify(ids)
    }).then(response => {
        if(response.ok){
            return response.json();
        }else{
            console.log("Error al eliminar");
        }
    }).catch(error => {
        console.log("Error: ",error);
    });
}

async function  eliminarDispositivos(){
    let table = document.querySelector("table");
    let tbody = table?.querySelector("tbody");
    let selectedRows = rowsSelectedDocument.sort((rowA, rowB) => rowB - rowA);
    let ids = [];
    // Obtenemos los Id de los dispositivos seleccionados
    if(modeUpdate==false){
      if(tbody){
        for(let rowIndex of selectedRows){
          let id = tbody.rows[rowIndex-1].cells[0].querySelector('input') 
          ? tbody.rows[rowIndex-1].cells[0].querySelector('input')?.value 
          : tbody.rows[rowIndex-1].cells[0].textContent;
          if(id){
            ids.push(id);
          }
        }
      }
      // Haremos la petición para eliminar a la API y, 
      // mientras, se mostrará pantalla de carga.
      eliminarDispositivosResponse(ids);

      if(tbody){
        for (let rowIndex of selectedRows) {
          tbody.deleteRow(rowIndex - 1);
        }
      }
      rowsSelectedDocument = [];
      contarSeleccionados();
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

function abrirModal(respuestaServidor){
    let modal = document.getElementById("modal-mensajes");
    let fade = document.createElement("div");
    let modalBody = document.getElementById("modal-body");
    let btnCerrar = document.getElementById("btn-cerrar");
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
    }else{
        for(let i = 0; i < respuestaServidor.message.length; i++){
            modalBody.innerHTML += `<div class="alert alert-danger" role="alert">
            ${respuestaServidor.message[i]}
            </div>`;
        }
    }
}

function getData(e){
    e.preventDefault();
    let formulario = document.getElementById("crear-dispositivo");
    if(formulario.checkValidity()){   
        let formData = new FormData(formulario);
        let dataDispositivo = {
            ip: formData.get("ip"),
            puerto: formData.get("puerto"),
            habitacion: formData.get("habitacion"),
            cama: formData.get("cama"),
            tipo: formData.get("tipo")
        };
        let mensajesValidaciones = validarCampos(dataDispositivo);
        if(mensajesValidaciones.length == 0){
            postDispositivo(dataDispositivo).then(data => {
                abrirModal(data);
                formulario.reset();
                mostrarAsistentes();
            });
        }else{
            abrirModal({"success":false,"message":mensajesValidaciones});
        }
    }else{
        formulario.reportValidity();
    }
}

function validarCampos(dataDispositivo){
    let mensajes = [];
    if(validarIp(dataDispositivo.ip) == false){
        mensajes.push("La dirección IP ingresada no es válida.");
    }
    return mensajes;
}


function validarIp(ip) {
    let octetos = ip.split('.');
    if (octetos.length !== 4) {
        return false;
    }
    for (let i = 0; i < octetos.length; i++) {
        let octeto = octetos[i];
        if (isNaN(octeto) || octeto < 0 || octeto > 255 || octeto.trim() === '') {
            return false;
        }
        if (octeto !== String(Number(octeto))) {
            return false;
        }
    }
    return true;
}

async function postDispositivo(data){
    let url = "/asistencias/dispositivos";
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