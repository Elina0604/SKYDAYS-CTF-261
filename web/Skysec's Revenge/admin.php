<?php
session_start();
if (!isset($_SESSION["logged_in"])) {
    header("Location: index.php");
    exit();
}

$error = "";
$success = "";

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    if (isset($_FILES["file"]) && $_FILES["file"]["error"] == UPLOAD_ERR_OK) {
        $file = $_FILES["file"];
        $filename = $file["name"];
        $contents = file_get_contents($file["tmp_name"]);

        // Uploads dizinini kontrol et ve oluştur
        if (!is_dir('./uploads/')) {
            mkdir('./uploads/', 0755, true);
        }

        if (stripos($filename, ".php") !== false) {
            $error = "PHP files are not allowed for security reasons.";
        }
        else if (stripos($contents, "<?php") !== false) {
            $error = "File contains unsafe PHP content.";
        }
        else {
            $upload_path = "./uploads/" . $filename;
            if (move_uploaded_file($file["tmp_name"], $upload_path)) {
                $success = "File uploaded successfully! <a href='/uploads/$filename' style='color: #2d5be3;'>View uploaded file</a>";
            } else {
                $error = "File upload failed.";
            }
        }
    } else {
        $error = "Please select a file to upload.";
    }
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Panel | System Management</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        body {
            background: #000000;
            color: #ffffff;
            min-height: 100vh;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        header {
            background: #111111;
            padding: 25px;
            border: 1px solid #222222;
            border-radius: 8px;
            margin-bottom: 30px;
        }
        
        .logo {
            font-size: 1.8rem;
            font-weight: 300;
            color: #ffffff;
            margin-bottom: 10px;
        }
        
        .nav {
            display: flex;
            gap: 20px;
            margin-top: 20px;
        }
        
        .nav a {
            color: #2d5be3;
            text-decoration: none;
            padding: 8px 16px;
            border: 1px solid #333333;
            border-radius: 4px;
            font-size: 0.9rem;
            transition: all 0.3s;
        }
        
        .nav a:hover {
            background: #2d5be3;
            color: #ffffff;
        }
        
        .content {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
        }
        
        .panel {
            background: #111111;
            padding: 30px;
            border: 1px solid #222222;
            border-radius: 8px;
        }
        
        .panel h2 {
            color: #ffffff;
            margin-bottom: 20px;
            font-weight: 400;
            font-size: 1.3rem;
            border-bottom: 1px solid #333333;
            padding-bottom: 10px;
        }
        
        .stats {
            font-size: 1rem;
            line-height: 1.8;
            color: #cccccc;
        }
        
        .upload-form input[type="file"] {
            width: 100%;
            padding: 12px;
            margin-bottom: 20px;
            background: #000000;
            border: 1px solid #333333;
            border-radius: 4px;
            color: #ffffff;
        }
        
        .upload-form input[type="submit"] {
            background: #2d5be3;
            color: #ffffff;
            padding: 12px 30px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-weight: 500;
            transition: background-color 0.3s;
        }
        
        .upload-form input[type="submit"]:hover {
            background: #1e4fd8;
        }
        
        .message {
            padding: 15px;
            margin: 20px 0;
            border-radius: 4px;
            text-align: center;
            font-size: 0.9rem;
        }
        
        .error {
            background: rgba(255, 0, 0, 0.1);
            border: 1px solid #cc0000;
            color: #ff6b6b;
        }
        
        .success {
            background: rgba(0, 255, 0, 0.1);
            border: 1px solid #00cc00;
            color: #90ee90;
        }
        
        .success a {
            color: #2d5be3;
            text-decoration: none;
            font-weight: 500;
        }
        
        .success a:hover {
            text-decoration: underline;
        }
        
        footer {
            text-align: center;
            margin-top: 50px;
            padding: 25px;
            color: #666666;
            border-top: 1px solid #222222;
            font-size: 0.85rem;
        }
        
        .system-info {
            background: rgba(45, 91, 227, 0.1);
            padding: 15px;
            border-radius: 4px;
            margin-top: 20px;
            border: 1px solid #2d5be3;
            font-size: 0.85rem;
        }
        
        .file-list {
            margin-top: 20px;
        }
        
        .file-list h3 {
            color: #cccccc;
            margin-bottom: 10px;
            font-size: 1rem;
        }
        
        .file-list ul {
            list-style: none;
            color: #888888;
        }
        
        .file-list li {
            padding: 5px 0;
            border-bottom: 1px solid #222222;
        }
        
        .file-list a {
            color: #2d5be3;
            text-decoration: none;
        }
        
        .file-list a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="logo">System Administration Panel</div>
            <p style="color: #888888; font-size: 0.9rem;">Welcome, Administrator</p>
            <div class="nav">
                <a href="/">Home</a>
                <a href="/admin.php">Dashboard</a>
                <a href="/uploads/">File Manager</a>
                <a href="#">Settings</a>
                <a href="logout.php">Log Out</a>
            </div>
        </header>
        
        <div class="content">
            <div class="panel">
                <h2>System Overview</h2>
                <div class="stats">
                    <?php
                        $uptime = @file_get_contents("/proc/uptime");
                        if ($uptime) {
                            $uptime = explode(" ", $uptime);
                            $uptime = $uptime[0];
                            $uptime = floor($uptime / 60);
                            echo "<p><strong>System Uptime:</strong> $uptime minutes</p>";
                        }
                        
                        $load = @sys_getloadavg();
                        if ($load) {
                            echo "<p><strong>Load Average:</strong> " . implode(", ", $load) . "</p>";
                        }
                        
                        echo "<p><strong>PHP Version:</strong> " . PHP_VERSION . "</p>";
                        echo "<p><strong>Server Time:</strong> " . date('Y-m-d H:i:s') . "</p>";
                    ?>
                </div>
                
                <div class="system-info">
                    <strong>Status:</strong> All systems operational. No issues detected.
                </div>

                <!-- Uploaded files list -->
                <div class="file-list">
                    <h3>Recently Uploaded Files</h3>
                    <?php
                    if (is_dir('./uploads/')) {
                        $files = scandir('./uploads/');
                        echo "<ul>";
                        foreach ($files as $file) {
                            if ($file != "." && $file != "..") {
                                echo "<li><a href='/uploads/$file' target='_blank'>$file</a></li>";
                            }
                        }
                        echo "</ul>";
                    }
                    ?>
                </div>
            </div>
            
            <div class="panel">
                <h2>File Management</h2>
                
                <?php if (!empty($error)): ?>
                    <div class="message error"><?php echo $error; ?></div>
                <?php endif; ?>
                
                <?php if (!empty($success)): ?>
                    <div class="message success"><?php echo $success; ?></div>
                <?php endif; ?>
                
                <form method="POST" action="admin.php" enctype="multipart/form-data" class="upload-form">
                    <label style="color: #cccccc; margin-bottom: 10px; display: block;">Select file to upload:</label>
                    <input type="file" name="file" required>
                    <br>
                    <input type="submit" value="Upload File">
                </form>
                
                <div style="margin-top: 20px; font-size: 0.85rem; color: #888888;">
                    <p>Allowed file types: Images, documents, archives</p>
                    <p>Maximum file size: 10MB</p>
                </div>
            </div>
        </div>
        
        <footer>
            <p>&copy; 2025 System Administration. All rights reserved.</p>
            <p style="margin-top: 8px;">Secure Admin Panel v4.2.1 | Last updated: <?php echo date('F Y'); ?></p>
        </footer>
    </div>
</body>
</html>