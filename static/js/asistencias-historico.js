let canvas = document.getElementById("myChart");
let ctx = canvas.getContext("2d");
let meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 
            'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'];
let historico = [];
let myChart = new Chart(ctx,{
    type:"line",
    data:{
        labels:meses,
        datasets: [{
            label: 'Histórico de asistencias',
            data: [],
            fill: false,
            borderColor: 'rgb(75, 192, 192)',
            tension: 0.1
          }]
    },
    options:{
        maintainAspectRatio: false,
        responsive:true,
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

mostrarHistorico();
function mostrarHistorico(desde="",hasta=""){
    
    let opcionMes = document.getElementById("pormes");
    // Cada objeto JSON es un mes de asistencias
    obtenerHistorico(desde,hasta).then(data => {
        historico = data;
        if(opcionMes.checked){
            myChart.data.labels = [];
            myChart.data.datasets[0].data = [];
            data.forEach(element => {
                myChart.data.labels.push(element.anio+ "-" +meses[element.mes-1]);
                myChart.data.datasets[0].data.push(element.total_asistencias);
            });
            myChart.update();
        }else{
            cambioAnio();
        }
    });
}

async function obtenerHistorico(desde="",hasta=""){
    let endpoint = "/api/asistencias/historico";
    if(desde != "" && hasta != ""){
        endpoint = endpoint+`?desde=${desde}&hasta=${hasta}`;
    }
    return await fetch(endpoint,{
        method:"GET",
        headers:{
            "Content-Type":"application/json"
        },
    }).then(data => {
        return data.json();
    }).catch(error => {
        console.log("Error: ",error);
    });
}

function filtroMes(){
    let inputDesde = document.getElementById("desde");
    let inputHasta = document.getElementById("hasta");
    if(inputDesde.value != "" && inputHasta.value != ""){
        mostrarHistorico(inputDesde.value,inputHasta.value);
    }
}

function cambioAnio(){
    let cambioAnios = [];
    let asistenciasAnios = [];
    historico.forEach(element => {
        if(!cambioAnios.includes(element.anio)){
            cambioAnios.push(element.anio);
        }
    });
    cambioAnios.forEach(anioActual => {
        let nAsistenciasAnio = 0;
        historico.forEach(asistenciaMes => {    
            if(anioActual == asistenciaMes.anio){
                nAsistenciasAnio += asistenciaMes.total_asistencias;
            }
        });
        asistenciasAnios.push(nAsistenciasAnio);
    });
    myChart.data.labels = cambioAnios;
    myChart.data.datasets[0].data = asistenciasAnios;
    myChart.update();
}

function cambioMes(){
    myChart.data.labels = [];
    myChart.data.datasets[0].data = [];
    historico.forEach(element => {
        myChart.data.labels.push(element.anio+ "-" +meses[element.mes-1]);
        myChart.data.datasets[0].data.push(element.total_asistencias);
    });
    myChart.update();
}