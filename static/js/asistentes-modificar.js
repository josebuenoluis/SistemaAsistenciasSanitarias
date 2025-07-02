let rowsSelectedDocument = [];
let modeUpdate = false;
let rowsUpdateValues = [];
let plantas = [];

obtenerPlantas().then(data => {
    if(data){
        plantas = data;
    }
})

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

function actualizarAsistentes(){
    let table = document.querySelector("table");
    let tbody = table?.querySelector("tbody");
    let headers = table?.querySelectorAll("thead th");
    // Iteramos en los seleccionados para cambiar sus 
    // campos por inputs editables.
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
        // Comenzamos a convertir sus campos en inputs editables.
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
              if(header=="NºPlanta"){
                let valorPlanta = values.find(element => element.index == rowIndex)["NºPlanta"];
                plantas.forEach(planta => {
                  let option = document.createElement("option");
                  option.value = planta.numero;
                  option.textContent = "Planta "+planta.numero;
                  selectOptions.appendChild(option);
                })
                selectOptions.value = valorPlanta.split(" ")[1];
                cellSelect.appendChild(selectOptions);
              }else{
                let input = document.createElement("input");
                input.type = "text";
                input.className = "form-control text-center";
                cellSelect.appendChild(input);
                values.forEach(element => {
                  if(element.index == rowIndex){
                    if(header == "NIF"){
                      input.value = element["NIF"];
                      input.readOnly = true;
                    }else if(header == "Nombre"){
                      input.value = element["Nombre"];
                    }else if(header == "Telefono"){
                      input.value = element["Telefono"];
                    }else if(header == "Codigo"){
                      input.value = element["Codigo"];
                      input.maxLength = 6;
                    }else if(header == "Estado"){
                      input.value = element["Estado"] == "True" ? "Activo" : "Inactivo";
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

function limpiarSeleccion() {
    let table = document.querySelector("table");
    let tbody = table.querySelector("tbody");
    let selectedRows = rowsSelectedDocument.sort((rowA, rowB) => rowB - rowA);
    if(tbody){
      for (let rowIndex of selectedRows) {
        let rowSelect = tbody.rows[rowIndex-1];
        rowSelect.onclick = (event) => seleccionarAsistente(event);
        for(let cell = 0; cell < rowSelect.cells.length;cell++){
          if(rowSelect.cells[cell].style.background == 'rgb(170, 190, 192)'){
            rowSelect.cells[cell].style.background = "";
          }
        }
    // Obtenemos los valores de las celdas en el update si los hay, 
    // para eliminar inputs de edición y reasignar textContent con sus valores. 
    // Mediante el atributo index, debemos asegurarnos de que 
    // estamos asignando la row indicada.
    if(rowsUpdateValues.length > 0){
      let table = document.querySelector("table");
      let headers = table?.querySelectorAll("thead th");
      if(headers){
        rowsUpdateValues.forEach(element =>{
          if(element.index == rowSelect.rowIndex){
            for(let cell = 0; cell < rowSelect.cells.length;cell++){
              let header = headers[cell].textContent;
              let cellUpdate = rowSelect.cells[cell];
              let childCell = cellUpdate.firstElementChild;
              if(childCell){
                cellUpdate.removeChild(childCell);
                if(header){
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

async function obtenerPlantas(){
    return await fetch("/api/plantas",{
        method:"GET",
        headers:{
            "Content-Type":"application/json"
        },
    }).then(response => {
        if(response.ok){
            return response.json();
        }else{
            console.error("Error al obtener las plantas: ",response.statusText);
        }
    }).catch(error => {
        console.log("Error: ",error);
    })
}

function buscarAsistentes(){
    let table = document.querySelector("table");
    let tbody = table.querySelector('tbody');
    let input = document.getElementById("buscar-asistentes");
    if(tbody){
      let rows = tbody.rows;
      for (let row = 0; row < rows.length; row++) {
        let rowTable = rows[row];
        let refRowTable = rowTable.cells[1].textContent?.toLowerCase() || '';
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

function clearTable(){
    let table = document.querySelector("table");
    let tbody = table.querySelector("tbody");
    if (tbody) {
      while (tbody.firstChild) {
        tbody.removeChild(tbody.firstChild);
      }
    }
}

async function updateResponse(dataAsistentes) {
  await fetch(`/asistentes/modificar`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(dataAsistentes),
  })
    .then((response) => {
      if (response.ok) {
        console.log("Actualizado correctamente");
      } else {
        console.log("Error al actualizar");
      }
    })
    .catch((error) => {
      console.log(error);
    });
}

async function saveUpdate(){
  let table = document.querySelector("table");
  let tbody = table.querySelector("tbody");
  let btnDelete = document.getElementById("btn-delete");
  let rowsUpdate = [];
  if(tbody){
    for(let rowIndex of rowsSelectedDocument){
      let rowSelect = tbody.rows[rowIndex-1];
      let nif = rowSelect.cells[0].querySelector('input') 
      ? rowSelect.cells[0].querySelector('input')?.value 
      : rowSelect.cells[0].textContent;
      let nombre = rowSelect.cells[1].querySelector('input') 
      ? rowSelect.cells[1].querySelector('input')?.value 
      : rowSelect.cells[1].textContent;
      let telefono = rowSelect.cells[2].querySelector('input') 
      ? rowSelect.cells[2].querySelector('input')?.value 
      : rowSelect.cells[2].textContent;
      let codigo = rowSelect.cells[3].querySelector('input') 
      ? rowSelect.cells[3].querySelector('input')?.value 
      : rowSelect.cells[3].textContent;
      let planta = rowSelect.cells[4].querySelector('select') 
      ? rowSelect.cells[4].querySelector('select')?.value 
      : rowSelect.cells[4].textContent;
      let estado = rowSelect.cells[5].querySelector('input') 
      ? rowSelect.cells[5].querySelector('input')?.value 
      : rowSelect.cells[5].textContent;
      estado = estado == "Activo" ? true : false;
      let asistente = {
          "nif":nif,
          "nombre":nombre,
          "telefono":telefono,
          "codigo":codigo,
          "planta":planta,
          "estado":estado
      }
      rowsUpdate.push(asistente);
    }
    updateResponse(rowsUpdate);
    // Luego de actualizar los productos, mostramos nuevamente la tabla
    // con los productos actualizados.
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
    });
  }
}


async function obtenerAsistentes(){
    return await fetch("/api/asistentes",{
        method:"GET",
        headers:{
            "Content-Type":"application/json"
        },
    }).then(response => {
        if(response.ok){
            return response.json();
        }else{
            console.error("Error al obtener los asistentes");
        }
    }).catch(error => {
        console.log("Error: ",error);
    })
}

async function mostrarAsistentes(){
    let table = document.querySelector("table");
    let tbody = table.querySelector("tbody");
    obtenerAsistentes().then(data => {
      data.forEach(element => {
        let newRow = document.createElement("tr");
        newRow.onclick = (event) => seleccionarAsistente(event);
        let cellNif = document.createElement("td");
        cellNif.textContent = element.dni;
        newRow.appendChild(cellNif);
        let cellNombre = document.createElement("td");
        cellNombre.textContent = element.nombre;
        newRow.appendChild(cellNombre);
        let cellTelefono = document.createElement("td");
        cellTelefono.textContent = element.telefono;
        newRow.appendChild(cellTelefono);
        let cellCodigo = document.createElement("td");
        cellCodigo.textContent = element.codigo;
        newRow.appendChild(cellCodigo);
        let cellPlanta = document.createElement("td");
        cellPlanta.textContent = "Planta "+element.planta_fk;
        newRow.appendChild(cellPlanta);
        let cellEstado = document.createElement("td");
        cellEstado.textContent = element.estado == "True" ? "Activo" : "Inactivo";
        newRow.appendChild(cellEstado);
        tbody?.appendChild(newRow);
      })
    })
  }

async function  eliminarAsistentes(){
    let table = document.querySelector("table");
    let tbody = table?.querySelector("tbody");
    let selectedRows = rowsSelectedDocument.sort((rowA, rowB) => rowB - rowA);
    let nifs = [];
    // Obtenemos los Id de los asistentes seleccionados
    if(modeUpdate==false){
      if(tbody){
        for(let rowIndex of selectedRows){
          let nif = tbody.rows[rowIndex-1].cells[0].querySelector('input') 
          ? tbody.rows[rowIndex-1].cells[0].querySelector('input')?.value 
          : tbody.rows[rowIndex-1].cells[0].textContent;
          if(nif){
            nifs.push(nif);
          }
        }
      }
      eliminarAsistentesResponse(nifs);

      if(tbody){
        for (let rowIndex of selectedRows) {
          tbody.deleteRow(rowIndex - 1);
        }
      }
      rowsSelectedDocument = [];
      contarSeleccionados();
    }
}

async function eliminarAsistentesResponse(nifs){
    return await fetch("/asistentes/modificar",{
        method:"DELETE",
        headers:{
            "Content-Type":"application/json"
        },
        body: JSON.stringify(nifs)
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