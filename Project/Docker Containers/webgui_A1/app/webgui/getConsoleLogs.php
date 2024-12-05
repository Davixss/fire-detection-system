<?php

header("Content-type: application/json");

$hostname = "10.24.104.16";
$port = 3307; 
$user = "root";
$pass = "smartcity";
$dbname = "smartcity";

// Database connection
try {
    $db = new PDO("mysql:host=$hostname;port=$port;dbname=$dbname", $user, $pass);
} catch (PDOException $e) {
    echo json_encode("DB Error: " . $e->getMessage());
    exit;
}


// Retrieve data
try {
    $logs = $db->query("SELECT * FROM logs ORDER BY datetime DESC");
    $logsData = $logs->fetchAll(PDO::FETCH_ASSOC);

    $result = [
        "logs" => $logsData
    ];

    echo json_encode($result, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
    
} catch (PDOException $e) {
    echo json_encode(["error" => $e->getMessage()]);
    die();
}


?>