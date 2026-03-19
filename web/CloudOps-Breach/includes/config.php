<?php
/**
 * DevOps Portal - Configuration & Session Management
 * Corporate IT Infrastructure Management System
 */

// Start session if not already started
if (session_status() === PHP_SESSION_NONE) {
    session_start();
}

// Check if user is logged in
function requireLogin() {
    if (!isset($_SESSION["logged_in"]) || $_SESSION["logged_in"] !== true) {
        header("Location: /index.php");
        exit();
    }
}

// Get current user info
function getCurrentUser() {
    return isset($_SESSION["username"]) ? $_SESSION["username"] : "Administrator";
}

// Portal configuration
define('PORTAL_NAME', 'CloudOps DevOps Portal');
define('PORTAL_VERSION', '3.2.1');
define('COMPANY_NAME', 'CloudOps Technologies Inc.');
define('CURRENT_YEAR', date('Y'));

// Get current page name for active navigation
function getCurrentPage() {
    $page = basename($_SERVER['PHP_SELF'], '.php');
    return $page;
}
?>
