<?php
$db_username = "root";
$db_password = "";
$db_name = "DB_brago";
$db_host = "localhost";

$tableName = 'tb_qrcode';
$columnName = 'name';

// Get the model name from the query string
$modelName = isset($_GET['modelName']) ? $_GET['modelName'] : '';

// Initialize the response array
$response = array();

try {
    // Create a PDO connection to the MySQL database
    $pdo = new PDO("mysql:host=$db_host;dbname=$db_name", $db_username, $db_password);

    // Set the PDO error mode to exception
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    // Modify the SQL query to fetch the desired columns
    $statement = $pdo->prepare("SELECT name, id, img_model, img_orientation,stl_name FROM $tableName WHERE $columnName = :modelName");
    $statement->bindParam(':modelName', $modelName, PDO::PARAM_STR);
    $statement->execute();

    // Fetch the result
    $result = $statement->fetch(PDO::FETCH_ASSOC);

    // Check if the model name exists
    if ($result) {
        // If the model exists, send the information in the response
        $response['name'] = $result['name'];
        $response['id'] = $result['id'];
        $response['img_model'] = $result['img_model'];
        $response['img_orientation'] = $result['img_orientation'];
        $response['stl_name'] = $result['stl_name'];
    } else {
        // If the model doesn't exist, send an error message in the response
        $response['error'] = 'Model not found';
    }
} catch (PDOException $e) {
    // If there is an error with the database connection or query, send an error message in the response
    $response['error'] = 'Database error: ' . $e->getMessage();
}

// Log the response for debugging
error_log(json_encode($response));

// Set the content type header to JSON
header('Content-Type: application/json');

// Print to the browser console
echo json_encode($response);