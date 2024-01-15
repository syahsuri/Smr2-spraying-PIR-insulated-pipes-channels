<?php
session_start();

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = $_POST['username'];
    $password = $_POST['password'];

    if (empty($username) || empty($password)) {
        $_SESSION['login_message'] = "Empty username or password.";
        $_SESSION['login_alert_type'] = "danger";
        header("Location: ../../login.php");
        exit();
    }

    require_once('db_connection.php');

    $query = "SELECT * FROM users WHERE username = ? AND password = ?";
    $stmt = $conn->prepare($query);
    $stmt->bind_param("ss", $username, $password);
    $stmt->execute();
    $result = $stmt->get_result();

    if ($result->num_rows > 0) {
        $_SESSION['username'] = $username;
        $_SESSION['login_message'] = "Login successful!";
        $_SESSION['login_alert_type'] = "success";
        sleep(2);
        header("Location: ../../main.php");
        exit();
    } else {
        $_SESSION['login_message'] = "Incorrect username or password.";
        $_SESSION['login_alert_type'] = "danger";
        header("Location: ../../login.php");
        exit();
    }
}
