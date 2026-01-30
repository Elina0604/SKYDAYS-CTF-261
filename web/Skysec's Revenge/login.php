<?php
    error_reporting(0);
    session_start();
    $admin_password = bin2hex(random_bytes(16));
    
    if ($_SERVER["REQUEST_METHOD"] == "POST") {
        $username = $_POST["username"];
        $password = $_POST["password"];
        
        if ($username == "skysec" && strcmp($admin_password, $password) == 0) {
            $_SESSION["logged_in"] = true;
            header("Location: admin.php");
            exit();
        }
    }
    
    header("Location: index.php");
?>