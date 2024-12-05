<!DOCTYPE html>
<html>
    <head>
        <title>SmartCity - Fire Recognition System</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="style.css?v=<?php echo time(); ?>">
        <script src="https://code.jquery.com/jquery-3.7.1.js" integrity="sha256-eKhayi8LEQwp4NKxN+CfCh+3qOVUtJn3QNZ0TciWLP4=" crossorigin="anonymous"></script>
        <script src="https://code.jquery.com/mobile/1.4.5/jquery.mobile-1.4.5.js" integrity="sha256-1PYCpx/EXA36KN1NKrK7auaTylVyk01D98R7Ccf04Bc=" crossorigin="anonymous"></script>
        
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" crossorigin=""/>
        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" crossorigin=""></script>
    </head>
    
    <body>
    
    	<div class="today-card">
        	<h1>Messina Smart City | Fire Detecting System</h1>
            <p>
            	<?php 
                	date_default_timezone_set('Europe/Rome');
                    $giorno = date("l");
                    $mese = date("F");
                    $data = date("d") . " " . $mese . " " . date("Y");
                    echo ucfirst($giorno) . ", " . $data;
                ?>
            </p>
        </div>

        <div class="map-container">
            <div class="info">
                <h1>Legenda</h1>
                <table width="100%">
                    <tr>
                        <td class="img"><img src="images/sensor_free.png" width="100%"></td>
                        <td>Free Sensor</td>
                    </tr>
                    <tr>
                        <td class="img"><img src="images/sensor_alarm.png" width="100%"></td>
                        <td>Alarmed Sensor</td>
                    </tr>
                    <tr>
                        <td class="img"><img src="images/actuator_free.png" width="100%"></td>
                        <td>Free Actuator</td>
                    </tr>
                    <tr>
                        <td class="img"><img src="images/actuator_busy.png" width="100%"></td>
                        <td>Busy Actuator</td>
                    </tr>
                </table>
            </div>
            <div id="map">
                <div id="map-1"></div>
            </div>
        </div>

        <div class="main-card">
            <center>
                <h1 style="font-size:22px; margin:0; margin-bottom:15px;">History Logs</h1>
			    <div class="console"></div>
            </center>
        </div>
        
        <!--<div class="main-card">
            <center>
			    <button id="btn-confirm" onclick="flaskRequest()">Alarm Reception Confirmation</button>
            </center>
        </div>-->
    
    </body>
    
    <script src="map.js?v=<?php echo time(); ?>" defer></script>
</html>