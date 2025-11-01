<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Secure Login | System Access</title>
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
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .login-container {
            background: #111111;
            padding: 50px;
            border: 1px solid #333333;
            border-radius: 8px;
            width: 100%;
            max-width: 400px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
        }
        
        .logo {
            text-align: center;
            margin-bottom: 40px;
        }
        
        .logo h1 {
            font-size: 2.2rem;
            color: #ffffff;
            font-weight: 300;
            letter-spacing: 1px;
            margin-bottom: 8px;
        }
        
        .logo p {
            color: #888888;
            font-size: 0.9rem;
            font-weight: 300;
        }
        
        .form-group {
            margin-bottom: 25px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 8px;
            color: #cccccc;
            font-size: 0.9rem;
            font-weight: 500;
        }
        
        .form-control {
            width: 100%;
            padding: 14px;
            background: #000000;
            border: 1px solid #333333;
            border-radius: 4px;
            color: #ffffff;
            font-size: 1rem;
            transition: border-color 0.3s;
        }
        
        .form-control:focus {
            outline: none;
            border-color: #555555;
        }
        
        .btn-login {
            width: 100%;
            padding: 14px;
            background: #2d5be3;
            color: #ffffff;
            border: none;
            border-radius: 4px;
            font-size: 1rem;
            font-weight: 500;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        
        .btn-login:hover {
            background: #1e4fd8;
        }
        
        .warning {
            background: rgba(255, 0, 0, 0.1);
            border: 1px solid #cc0000;
            color: #ff6b6b;
            padding: 12px;
            border-radius: 4px;
            margin-top: 25px;
            text-align: center;
            font-size: 0.85rem;
            line-height: 1.4;
        }
        
        .footer {
            text-align: center;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #222222;
            color: #666666;
            font-size: 0.8rem;
        }
        
        .language-select {
            text-align: center;
            margin-bottom: 20px;
        }
        
        .language-select select {
            background: #000000;
            border: 1px solid #333333;
            color: #ffffff;
            padding: 5px 10px;
            border-radius: 3px;
            font-size: 0.8rem;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <div class="language-select">
            <select>
                <option>English</option>
                <option>Español</option>
                <option>Français</option>
                <option>Deutsch</option>
            </select>
        </div>

        <div class="logo">
            <h1>System Access</h1>
            <p>Secure Authentication Portal</p>
        </div>
        
        <form method="POST" action="login.php">
            <div class="form-group">
                <label for="username">Username</label>
                <input type="text" id="username" name="username" class="form-control" placeholder="Enter your username" required>
            </div>
            
            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" class="form-control" placeholder="Enter your password" required>
            </div>
            
            <button type="submit" class="btn-login">Sign In</button>
        </form>
        
        <div class="warning">
            For security reasons, please do not use passwords from other services.
        </div>
        
        <div class="footer">
            <p>&copy; 2024 System Administration. All rights reserved.</p>
            <p style="margin-top: 8px;">Version 4.2.1</p>
        </div>
    </div>
</body>
</html>
