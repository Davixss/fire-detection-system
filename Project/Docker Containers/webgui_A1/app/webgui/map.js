$(document).ready(function()
{
    getMapData();
    getConsoleLogs();

    setInterval(function()
    {
        getMapData();
    }, 10000);

    setInterval(function()
    {
        getConsoleLogs();
    }, 2000);
});

function getMapData()
{
    // Call getMapData.php
    $.ajax({
        url: 'getMapData.php',  
        type: 'POST',
        dataType: 'json',  
        success: function(jsonData) {
            resetMap();
            generateMap(jsonData);
        },
        error: function(jqXHR, textStatus, errorThrown) {
            alert('Errore: ' + textStatus);
        }
    });
}

function getConsoleLogs()
{
    // Call getMapData.php
    $.ajax({
        url: 'getConsoleLogs.php',  
        type: 'POST',
        dataType: 'json',  
        success: function(jsonData) {
            if (jsonData.logs && Array.isArray(jsonData.logs)) {
                var consoleDiv = $('.console');
                consoleDiv.empty();
                jsonData.logs.forEach(function(log) {
                    if (log.message_type == 'ACTUATOR_ACTIVATED') {
                        var logText = `<p class='log-red'><strong>[${log.id}] ${log.datetime}</strong> &nbsp;&nbsp; ID Device: ${log.id_device} &nbsp;&nbsp; Message: ${log.message}</p>`;
                    } else {
                        var logText = `<p><strong>[${log.id}] ${log.datetime}</strong> &nbsp;&nbsp; ID Device: ${log.id_device} &nbsp;&nbsp; Message: ${log.message} </p>`;
                    }
                    consoleDiv.append(logText);
                });
            } else {
                alert("Nessun dato trovato.");
            }
        },
        error: function(jqXHR, textStatus, errorThrown) {
            alert('Errore: ' + textStatus);
        }
    });
}

function resetMap()
{
    document.getElementById('map-1').remove();

    // Ricrea l'elemento per la mappa
    const newMapContainer = document.createElement('div');
    newMapContainer.id = 'map-1';
    newMapContainer.style.height = '400px'; 
    document.getElementById('map').appendChild(newMapContainer);
}

function generateMap(jsonData)
{
    // Inizializza la mappa
    const map = L.map('map-1').setView([38.192231, 15.555286], 11); // Zoom su Messina

    // Aggiungi il layer di OpenStreetMap
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    // Marker attuatori liberi
    const actuatorFree = L.icon({
        iconUrl: './images/actuator_free.png', 
        shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
        iconSize: [30, 35], // Dimensione del marker
        iconAnchor: [15, 31], // Punto di ancoraggio
        popupAnchor: [9, -34], // Posizione del popup
        shadowSize: [41, 41]  // Dimensione dell'ombra
    });

    // Marker attuatori occupati
    const actuatorBusy = L.icon({
        iconUrl: './images/actuator_busy.png', 
        shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
        iconSize: [30, 35], // Dimensione del marker
        iconAnchor: [15, 31], // Punto di ancoraggio
        popupAnchor: [9, -34], // Posizione del popup
        shadowSize: [41, 41]  // Dimensione dell'ombra
    });

    // Marker sensori liberi
    const sensorFree = L.icon({
        iconUrl: './images/sensor_free.png', 
        shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
        iconSize: [30, 35], // Dimensione del marker
        iconAnchor: [15, 31], // Punto di ancoraggio
        popupAnchor: [9, -34], // Posizione del popup
        shadowSize: [41, 41]  // Dimensione dell'ombra
    });

    // Marker sensori in allarme
    const sensorAlarm = L.icon({
        iconUrl: './images/sensor_alarm.png', 
        shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
        iconSize: [30, 35], // Dimensione del marker
        iconAnchor: [15, 31], // Punto di ancoraggio
        popupAnchor: [9, -34], // Posizione del popup
        shadowSize: [41, 41]  // Dimensione dell'ombra
    });


    var jsonData = JSON.parse(JSON.stringify(jsonData));
    for (var i=0; i<jsonData['mapsensor'].length; i++)
    {
        let sensor = jsonData['mapsensor'][i];
        let iconValue;

        // Calcolo differenza in secondi
        let lastAlarm = new Date(sensor['last_alarm']); // Assumi che sia in formato ISO o timestamp
        let currentTime = new Date();
        let timeDifference = (currentTime - lastAlarm) / 1000 / 60; 

        if (timeDifference <= 2) { iconValue = sensorAlarm; } else { iconValue = sensorFree; }

        let popupText = `Sensor ${sensor['id_device']}: ${sensor['name']}<br>Last Alarm: ${sensor['last_alarm']}`;
        let coord_lat = sensor['coord_lat'];
        let coord_lon = sensor['coord_lon'];

        // Add marker to map
        L.marker([coord_lon, coord_lat], { icon: iconValue })
        .addTo(map)
        .bindPopup(popupText);
    }

    for (var i=0; i<jsonData['mapactuator'].length; i++)
    {
        let actuator = jsonData['mapactuator'][i];
        let status = 'Free';
        let iconValue;

        if (actuator['busy'] == 1){ iconValue = actuatorBusy; status = 'Busy'; } else { iconValue = actuatorFree; status = 'Free'; }
        let popupText = `Actuator ${actuator['id_device']}: ${actuator['name']}<br>Status: ${status}`;
        let coord_lat = actuator['coord_lat'];
        let coord_lon = actuator['coord_lon'];

        // Add marker to map
        L.marker([coord_lon, coord_lat], { icon: iconValue })
        .addTo(map)
        .bindPopup(popupText);
    }

    /* Disegna un percorso tra due punti
    const routeCoordinates = [
        [38.191809, 15.548264], // Punto S2
        [38.165161, 15.542471]  // Punto A1
    ];

    L.polyline(routeCoordinates, { color: 'blue' }).addTo(map)
        .bindPopup("Percorso tra S2 e A1"); */
}